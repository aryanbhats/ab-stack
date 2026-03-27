# todoist-sync

Automatic Todoist task tracking for Claude Code sessions.

Maps git repos to Todoist sections. Shows due tasks on session start. Offers to complete sub-tasks on session stop. Creates task chunks from plans.

## Install

```bash
# Add ab-stack marketplace (one-time)
# In ~/.claude/settings.json, add:
# "extraKnownMarketplaces": {
#   "ab-stack": { "source": { "source": "github", "repo": "aryanbhats/ab-stack" } }
# }

# Install the plugin
claude plugin install todoist-sync@ab-stack
```

Or test locally:
```bash
claude --plugin-dir ./plugins/todoist-sync
```

## Prerequisites

- [Todoist MCP](https://github.com/anthropics/claude-code) connected (`/mcp` > Todoist)
- Git repository for each project you want to track

## Setup

In each project you want to track:

```
/todoist-sync:setup
```

This will:
1. Detect your git repo
2. Let you pick a Todoist project and section
3. Create tracking labels (`quick-win`, `blocked`, `needs-design`)
4. Write config to persistent plugin storage
5. Show a preview of what session start will display

## How It Works

### Session Start (automatic)
When you open Claude Code in a configured repo, the plugin:
- Fetches overdue + due-this-week tasks from your Todoist section
- Shows a brief summary before you start working

### During Session
As you complete work, Claude:
- Marks sub-tasks as done in Todoist
- Updates parent task descriptions with branch name and progress
- Tracks which tasks were touched this session

### Session Stop (automatic)
When a session ends, the plugin:
- Summarizes what was completed
- Offers to update task descriptions with session context

### Plan-to-Task
When you exit plan mode, Claude offers to create matching Todoist chunks and sub-tasks from the plan steps.

## Labels

| Label | Color | Meaning |
|---|---|---|
| `quick-win` | Green | Completable in <30 min |
| `blocked` | Red | Waiting on external dependency |
| `needs-design` | Violet | Needs design thinking before coding |

## Config

Stored at `~/.claude/plugins/data/todoist-sync/config.json`. Managed by `/todoist-sync:setup` — no manual editing needed.

## Adding More Projects

Just `cd` into another repo and run `/todoist-sync:setup` again. Existing project mappings are preserved.
