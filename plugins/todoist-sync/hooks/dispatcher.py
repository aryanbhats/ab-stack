#!/usr/bin/env python3
"""todoist-sync dispatcher — single-process hook for SessionStart + Stop.

Resolves CWD to a configured project, outputs structured JSON for Claude Code.
Silent no-op if unconfigured, not in a git repo, or no matching project.

Fixes over the bash version:
- Single python3 invocation (~30ms total vs ~210ms for 7 spawns)
- json.dumps for all output (no shell interpolation → no JSON injection)
- Atomic writes via temp file + os.replace (no corrupt session files)
- Session keyed by session_id (no cross-session stomping)
- PROJECT_KEY sanitized (no path traversal via ../../)
"""

import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime


def get_git_info():
    """Get repo root and branch. Returns (None, None) if not in a git repo."""
    try:
        repo = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=5
        )
        if repo.returncode != 0:
            return None, None
        repo_root = repo.stdout.strip()

        branch_result = subprocess.run(
            ["git", "symbolic-ref", "--quiet", "--short", "HEAD"],
            capture_output=True, text=True, timeout=5
        )
        branch = branch_result.stdout.strip() if branch_result.returncode == 0 else "detached"

        return repo_root, branch
    except Exception:
        return None, None


def sanitize_key(key):
    """Sanitize project key for use in filenames. Strip path traversal."""
    # Remove any path components
    key = os.path.basename(key)
    # Only allow alphanumeric, hyphens, underscores
    key = re.sub(r'[^a-zA-Z0-9_-]', '_', key)
    return key or "unknown"


def atomic_write_json(path, data):
    """Write JSON atomically via temp file + os.replace."""
    dir_path = os.path.dirname(path)
    os.makedirs(dir_path, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(dir=dir_path, suffix=".tmp")
    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(data, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
    except Exception:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def read_json_safe(path, default=None):
    """Read JSON file, returning default on any error."""
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return default


def main():
    # Resolve data directory
    data_dir = os.environ.get(
        "CLAUDE_PLUGIN_DATA",
        os.path.expanduser("~/.claude/plugins/data/todoist-sync")
    )
    config_path = os.path.join(data_dir, "config.json")

    # Not configured — silent exit
    if not os.path.isfile(config_path):
        return

    # Must be in a git repo
    repo_root, branch = get_git_info()
    if not repo_root:
        return

    # Load config
    config = read_json_safe(config_path)
    if not config or "projects" not in config:
        return

    # Find matching project by resolved repo path
    real_repo = os.path.realpath(repo_root).rstrip("/")
    matched_key = None
    matched_proj = None

    for key, proj in config.get("projects", {}).items():
        configured = os.path.realpath(proj.get("repo", "")).rstrip("/")
        if configured == real_repo:
            matched_key = key
            matched_proj = proj
            break

    if not matched_key or not matched_proj:
        return

    # Extract project config
    section_id = matched_proj.get("section_id", "")
    section_name = matched_proj.get("section_name", "")
    max_tasks = config.get("preferences", {}).get("summary_max_tasks", 10)

    # Clamp and validate max_tasks
    try:
        max_tasks = int(max_tasks)
        max_tasks = max(1, min(100, max_tasks))
    except (TypeError, ValueError):
        max_tasks = 10

    # Read hook event from stdin
    try:
        hook_input = json.load(sys.stdin)
    except Exception:
        hook_input = {}

    event = hook_input.get("hook_event_name", "SessionStart")
    session_id = hook_input.get("session_id", "default")

    # Session state — keyed by session_id to prevent cross-session stomping
    safe_key = sanitize_key(matched_key)
    safe_session = sanitize_key(session_id)
    session_dir = os.path.join(data_dir, "sessions")
    session_file = os.path.join(session_dir, f"{safe_key}_{safe_session}.json")

    # Also keep a "latest" symlink/file per project for the SKILL.md to find easily
    latest_session = os.path.join(session_dir, f"{safe_key}_latest.json")

    if event == "SessionStart":
        state = {
            "project": matched_key,
            "repo": repo_root,
            "branch": branch,
            "section_id": section_id,
            "session_id": session_id,
            "started_at": datetime.now().isoformat(),
            "active_task_ids": [],
        }
        atomic_write_json(session_file, state)
        atomic_write_json(latest_session, state)

        output = {
            "systemMessage": f"[todoist-sync] Project '{matched_key}' mapped to Todoist section '{section_name}'.",
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": (
                    f"[todoist-sync] RESOLVED — skip all discovery. "
                    f"Call exactly: mcp__todoist__find-tasks({{sectionId: \"{section_id}\", limit: {max_tasks}}}). "
                    f"Do NOT call get-overview, search, find-projects, or find-sections — the section ID is already resolved. "
                    f"Filter the results to show overdue + due-this-week only. "
                    f"Branch: {branch}. Session: {session_file}"
                ),
            },
        }
        print(json.dumps(output))

    elif event == "Stop":
        # Check for stop_hook_active to prevent re-entry
        if hook_input.get("stop_hook_active"):
            return

        # Try session-specific file first, fall back to latest
        state = read_json_safe(session_file) or read_json_safe(latest_session)
        if not state:
            return

        active_ids = state.get("active_task_ids", [])

        output = {
            "hookSpecificOutput": {
                "hookEventName": "Stop",
                "additionalContext": (
                    f"[todoist-sync] Session ending for {matched_key} ({section_name}). "
                    f"Branch: {branch}. "
                    f"Active task IDs this session: {json.dumps(active_ids)}. "
                    f"Session file: {session_file}. "
                    f"Offer to complete active sub-tasks and update task descriptions with what was done this session."
                ),
            },
        }
        print(json.dumps(output))


if __name__ == "__main__":
    main()
