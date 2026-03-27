---
name: todoist-sync
description: |
  Dev task tracker synced to Todoist. Auto-triggered via hooks on SessionStart
  and Stop in configured projects. Fetches due tasks, completes sub-tasks after
  work, creates chunks from plans. Use /todoist-sync:setup to configure a project.
---

# todoist-sync

Keeps Todoist in sync with Claude Code sessions. Uses `mcp__todoist__*` MCP tools.

Config at `${CLAUDE_PLUGIN_DATA}/config.json` (written by `/todoist-sync:setup`).
Session state at `${CLAUDE_PLUGIN_DATA}/sessions/<project>.json`.

## On Session Start

The SessionStart hook injects context with: project key, section ID, branch, max tasks, session file path.

When you receive this context:

1. **Read session state** from the session file path provided
2. **Fetch tasks** via `mcp__todoist__find-tasks` with the `sectionId` from context
   - Limit to the `max_tasks` value from context
   - Include overdue tasks
3. **Show brief summary:**
   - Overdue tasks (flag with priority)
   - Due today / this week
   - Total open chunks vs sub-tasks
4. **If a task description mentions a branch**, note if it matches current branch

Keep it concise — 5-10 lines max. The user wants to start working, not read a report.

## During Session

### Completing sub-tasks
When a piece of work is done (code written, tests pass, PR merged):
1. Identify which Todoist sub-tasks were addressed
2. Complete them via `mcp__todoist__complete-tasks`
3. **Update session state** — add completed task IDs to `active_task_ids` in the session file:
   ```bash
   python3 -c "
   import json, sys
   with open(sys.argv[1]) as f:
       state = json.load(f)
   state['active_task_ids'].extend(sys.argv[2:])
   # Deduplicate
   state['active_task_ids'] = list(set(state['active_task_ids']))
   with open(sys.argv[1], 'w') as f:
       json.dump(state, f, indent=2)
   " "${CLAUDE_PLUGIN_DATA}/sessions/PROJECT_KEY.json" "TASK_ID_1" "TASK_ID_2"
   ```
4. If all sub-tasks of a parent chunk are done, ask if the chunk should be completed too

### Updating task descriptions
When significant progress is made, append session context to the parent chunk's description via `mcp__todoist__update-tasks`:

```
---
**Session: YYYY-MM-DD**
Branch: `branch-name`
Done: what was accomplished
Next: what remains
```

Append, don't replace existing description content.

## On Session Stop

The Stop hook injects context with: project key, section name, branch, active task IDs, session file path.

When you receive this context:
1. If `active_task_ids` is empty, skip — nothing was tracked this session
2. If tasks were tracked, briefly note what was completed
3. Offer to update any parent chunk descriptions with session context
4. Do NOT do a full section scan — only act on the active task IDs

## Creating Tasks from Plans

When a plan is written (plan mode exit) in a configured project:

1. **Offer** to create matching Todoist tasks (don't auto-create without asking)
2. Each major plan step becomes a **chunk** (parent task) in the project's section
3. Each sub-step becomes a **sub-task** under the chunk
4. Apply labels based on content:
   - `quick-win`: <30 min, targeted fix, single-file change
   - `blocked`: depends on external API, waiting on someone, infra not ready
   - `needs-design`: UI work, architecture decision, multiple valid approaches
5. Set priority:
   - `p1`: blocking other work
   - `p2`: due this week or next deliverable
   - `p3`: planned but not urgent
   - `p4`: backlog / nice-to-have
6. **Search before creating** — use `mcp__todoist__find-tasks` with `searchText` to avoid duplicates

## Task Naming Rules

- **Chunks:** verb + deliverable — "Build FastAPI backend", "Fix coverage page bug", "Merge Phase 2 branches"
- **Sub-tasks:** specific action — "Add test for endpoint", "Wire service to x_api.py", "Run full test suite"
- **Never vague:** no "Work on X", "Look into Y", "Investigate Z" — always specific and completable

## What Claude Manages vs User Manages

| Claude manages | User manages (phone/Todoist app) |
|---|---|
| Creating chunks + sub-tasks from plans | Due dates and deadlines |
| Completing sub-tasks after work | Reordering priorities |
| Applying labels based on context | Moving tasks between sections |
| Updating descriptions with session state | Recurring task schedules |
| Suggesting new tasks from TODOs/FIXMEs | Deleting tasks they don't want |

## Rules

1. **Never create duplicate tasks.** Search first via `mcp__todoist__find-tasks`.
2. **Never set due dates** unless the user explicitly asks or the plan has a deadline.
3. **Never delete tasks.** Only complete them or update them.
4. **Keep it lightweight.** Only sync at session boundaries and plan exits.
5. **Descriptions are breadcrumbs.** Branch names, state, context — so the user can pick up later.
6. **Sub-tasks are karma generators.** 3-6 per chunk. Each should feel like progress when checked off.
