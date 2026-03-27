---
name: setup
description: Interactive setup wizard for todoist-sync. Maps the current git repo to a Todoist project/section, creates tracking labels, and writes config. Run once per project.
---

# todoist-sync Setup

Configure Todoist tracking for the current git repository.

## Prerequisites

- Todoist MCP must be connected (`mcp__todoist__*` tools available)
- Must be inside a git repository

## Setup Flow

### Step 1: Verify Todoist connection

Run `mcp__todoist__get-overview` (no args). If it fails, tell the user:
"Todoist MCP is not connected. Run `/mcp` and connect to Todoist first, then try `/todoist-sync:setup` again."

### Step 2: Detect git repo

```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
REPO_NAME=$(basename "$REPO_ROOT")
```

If not in a git repo, tell the user: "Not in a git repository. `cd` into a project first."

### Step 3: Check existing config

```bash
DATA_DIR="${CLAUDE_PLUGIN_DATA:-$HOME/.claude/plugins/data/todoist-sync}"
CONFIG="$DATA_DIR/config.json"
cat "$CONFIG" 2>/dev/null || echo "NO_CONFIG"
```

If config exists, check if this repo is already mapped. If so, show current mapping and ask if they want to update it.

### Step 4: Pick Todoist project and section

1. Fetch all projects: `mcp__todoist__get-overview` (no projectId)
2. Show the user a list of projects with their sections
3. Ask: "Which project should `REPO_NAME` track tasks in?"
4. After project selection, ask: "Which section?" — or offer to create a new one via `mcp__todoist__add-sections`

### Step 5: Create labels (if missing)

Use `mcp__todoist__find-labels` to check if these exist:
- `quick-win` (lime_green)
- `blocked` (red)
- `needs-design` (violet)

Create any missing ones via `mcp__todoist__add-labels`.

### Step 6: Write config

```bash
mkdir -p "${CLAUDE_PLUGIN_DATA}/sessions"
```

Read existing config (or start fresh), add/update the project entry, write back:

```json
{
  "version": 1,
  "labels": {
    "quick-win": { "color": "lime_green" },
    "blocked": { "color": "red" },
    "needs-design": { "color": "violet" }
  },
  "projects": {
    "<repo-name>": {
      "repo": "<absolute-repo-path>",
      "todoist_project_id": "<selected-project-id>",
      "section_id": "<selected-section-id>",
      "section_name": "<selected-section-name>"
    }
  },
  "preferences": {
    "summary_max_tasks": 10,
    "auto_complete_subtasks": false
  }
}
```

Use `python3` to read/merge/write the JSON (don't clobber existing projects):

```bash
python3 -c "
import json, os, sys
data_dir = sys.argv[1]
config_path = os.path.join(data_dir, 'config.json')
# Read existing or start fresh
try:
    with open(config_path) as f:
        cfg = json.load(f)
except:
    cfg = {'version': 1, 'labels': {}, 'projects': {}, 'preferences': {'summary_max_tasks': 10, 'auto_complete_subtasks': False}}
# Merge new project (passed as JSON arg)
new_project = json.loads(sys.argv[2])
cfg['projects'][sys.argv[3]] = new_project
# Ensure labels
cfg['labels'] = {'quick-win': {'color': 'lime_green'}, 'blocked': {'color': 'red'}, 'needs-design': {'color': 'violet'}}
with open(config_path, 'w') as f:
    json.dump(cfg, f, indent=2)
print('Config written to', config_path)
" "$DATA_DIR" '{"repo":"REPO_PATH","todoist_project_id":"PROJ_ID","section_id":"SEC_ID","section_name":"SEC_NAME"}' "REPO_KEY"
```

Replace the placeholder values with actual selections.

### Step 7: Dry run

Fetch tasks for the selected section via `mcp__todoist__find-tasks` with `sectionId`. Show:
- Number of open tasks
- Any overdue tasks
- Tasks due this week

Tell the user: "todoist-sync is configured for `REPO_NAME`. On your next session start, you'll see this summary automatically."

## Adding More Projects

If the user runs `/todoist-sync:setup` in a different repo, repeat steps 2-7. The config merges — existing project entries are preserved.
