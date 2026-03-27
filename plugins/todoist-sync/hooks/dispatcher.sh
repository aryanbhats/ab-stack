#!/bin/bash
# todoist-sync dispatcher — single hook for SessionStart + Stop
# Resolves CWD to a configured project, outputs structured context for Claude.
# Silent no-op if unconfigured or not in a tracked repo.
set -euo pipefail

DATA_DIR="${CLAUDE_PLUGIN_DATA:-$HOME/.claude/plugins/data/todoist-sync}"
CONFIG="$DATA_DIR/config.json"

# Not configured yet — silent exit (user needs to run /todoist-sync:setup)
[ -f "$CONFIG" ] || exit 0

# Must be in a git repo
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
BRANCH=$(git branch --show-current 2>/dev/null || echo "detached")

# Find matching project by resolved repo path
MATCH=$(python3 -c "
import json, sys, os
with open(sys.argv[1]) as f:
    cfg = json.load(f)
repo = os.path.realpath(sys.argv[2]).rstrip('/')
for key, proj in cfg.get('projects', {}).items():
    configured = os.path.realpath(proj.get('repo', '')).rstrip('/')
    if configured == repo:
        print(json.dumps({'key': key, **proj}))
        sys.exit(0)
sys.exit(1)
" "$CONFIG" "$REPO_ROOT" 2>/dev/null) || exit 0

# Parse matched project
PROJECT_KEY=$(echo "$MATCH" | python3 -c "import json,sys; print(json.load(sys.stdin)['key'])")
SECTION_ID=$(echo "$MATCH" | python3 -c "import json,sys; print(json.load(sys.stdin)['section_id'])")
SECTION_NAME=$(echo "$MATCH" | python3 -c "import json,sys; print(json.load(sys.stdin)['section_name'])")
MAX_TASKS=$(python3 -c "
import json, sys
with open(sys.argv[1]) as f:
    cfg = json.load(f)
print(cfg.get('preferences', {}).get('summary_max_tasks', 10))
" "$CONFIG" 2>/dev/null || echo "10")

# Read hook event from stdin JSON
INPUT=$(cat)
EVENT=$(echo "$INPUT" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(data.get('hook_event_name', 'SessionStart'))
except:
    print('SessionStart')
" 2>/dev/null || echo "SessionStart")

# Session state directory
SESSION_DIR="$DATA_DIR/sessions"
mkdir -p "$SESSION_DIR"
SESSION_FILE="$SESSION_DIR/${PROJECT_KEY}.json"

case "$EVENT" in
  SessionStart)
    # Write fresh session state
    python3 -c "
import json, datetime, sys
state = {
    'project': sys.argv[1],
    'repo': sys.argv[2],
    'branch': sys.argv[3],
    'section_id': sys.argv[4],
    'started_at': datetime.datetime.now().isoformat(),
    'active_task_ids': []
}
with open(sys.argv[5], 'w') as f:
    json.dump(state, f, indent=2)
" "$PROJECT_KEY" "$REPO_ROOT" "$BRANCH" "$SECTION_ID" "$SESSION_FILE"

    cat <<EOF
{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"[todoist-sync] Project: $PROJECT_KEY ($SECTION_NAME). Section ID: $SECTION_ID. Branch: $BRANCH. Max tasks: $MAX_TASKS. Session file: $SESSION_FILE. Use mcp__todoist__find-tasks with sectionId=$SECTION_ID to fetch overdue + due-this-week tasks (limit $MAX_TASKS). Show a brief summary of what's due before starting work."}}
EOF
    ;;

  Stop)
    # Only act if we have session state
    [ -f "$SESSION_FILE" ] || exit 0

    ACTIVE_IDS=$(python3 -c "
import json, sys
with open(sys.argv[1]) as f:
    state = json.load(f)
print(json.dumps(state.get('active_task_ids', [])))
" "$SESSION_FILE" 2>/dev/null || echo "[]")

    cat <<EOF
{"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"[todoist-sync] Session ending for $PROJECT_KEY ($SECTION_NAME). Branch: $BRANCH. Active task IDs this session: $ACTIVE_IDS. Session file: $SESSION_FILE. Offer to complete active sub-tasks and update task descriptions with what was done this session."}}
EOF
    ;;
esac
