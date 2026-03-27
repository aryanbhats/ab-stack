# Handoff: todoist-sync Plugin — Built, Tested, Deployed
- Branch: main (ab-stack repo) | 2026-03-27

## State
Built and shipped `todoist-sync` as a Claude Code plugin in the ab-stack marketplace. The plugin auto-tracks Todoist tasks at session boundaries — SessionStart shows due tasks, Stop summarizes session. Fully tested, Codex-reviewed (v1.1.0), and permanently installed.

**What was built this session:**
1. Todoist task structure — 12 chunks, 36 sub-tasks across 3 projects (AB Index, BMO GAM RAG, NV Chase) with labels (quick-win, blocked, needs-design)
2. todoist-sync plugin — hooks, skills, dispatcher.py, setup wizard, packaged as Claude Code plugin
3. ab-stack marketplace — `.claude-plugin/marketplace.json` added, ab-stack is now a plugin marketplace
4. Codex adversarial review — 8 findings, all fixed in v1.1.0 rewrite (bash→python dispatcher)

**Current status:**
- Plugin works end-to-end: SessionStart systemMessage shows, `/todoist-sync:todoist-sync` makes exactly 1 MCP call scoped to correct section, Stop hook fires cleanly
- Permanently installed via `extraKnownMarketplaces` + `enabledPlugins` in `~/.claude/settings.json`
- Config exists at `~/.claude/plugins/data/todoist-sync/config.json` (and copies at `-inline` and `-ab-stack` variants for different load methods)

## Files & Decisions
| Item | Details |
|------|---------|
| `ab-stack/.claude-plugin/marketplace.json` | NEW — makes ab-stack a plugin marketplace |
| `ab-stack/plugins/todoist-sync/.claude-plugin/plugin.json` | Plugin manifest v1.1.0, no userConfig (was dead) |
| `ab-stack/plugins/todoist-sync/hooks/dispatcher.py` | Single-process Python dispatcher — json.dumps output, atomic writes, session_id keying, sanitized keys, stop_hook_active guard |
| `ab-stack/plugins/todoist-sync/hooks/dispatcher.sh` | OLD bash version — kept in repo but hooks.json points to .py |
| `ab-stack/plugins/todoist-sync/hooks/hooks.json` | SessionStart + Stop hooks pointing to dispatcher.py |
| `ab-stack/plugins/todoist-sync/skills/todoist-sync/SKILL.md` | Main skill — Step 0 reads config, exactly 1 MCP call with sectionId |
| `ab-stack/plugins/todoist-sync/skills/setup/SKILL.md` | Interactive setup wizard via MCP |
| `~/.claude/settings.json` | Added extraKnownMarketplaces (ab-stack) + enabledPlugins (todoist-sync@ab-stack) + mcp__todoist__* permissions |
| `~/.claude/plugins/data/todoist-sync/config.json` | 3 projects mapped: the-ab-index, bmo-gam-rag, sb-nv-chase |
| Decision: dispatcher.py not .sh | Codex found 7x python3 spawns (435ms), JSON injection, path traversal. Python rewrite: 108ms, safe output, atomic writes |
| Decision: session_id keying | Sessions keyed by `project_session-id` not just project — prevents cross-session stomping |
| Decision: Stop uses systemMessage | hookSpecificOutput is invalid for Stop events — only top-level fields (decision, systemMessage) are accepted |
| Decision: additionalContext is a hint | Model ignores it for task fetching. Skill invocation (`/todoist-sync:todoist-sync`) is the reliable path. Hook's job is state setup + systemMessage reminder |
| Decision: config in 3 data dirs | `--plugin-dir` uses `todoist-sync-inline`, marketplace uses `todoist-sync-ab-stack`, manual uses `todoist-sync`. Config copied to all 3 |

## Next Steps
1. Clean up old `dispatcher.sh` from the repo (hooks.json already points to .py)
2. Make `/todoist-sync:setup` work so new users don't need manual config.json creation
3. Test the setup skill end-to-end in a fresh project
4. Consider submitting to official Anthropic marketplace once battle-tested
5. Add plan-exit hook — when exiting plan mode, offer to create Todoist chunks from plan steps (currently only in SKILL.md instructions, not wired to a hook)
6. Investigate making SessionStart auto-invoke the skill (currently just injects context that model ignores — need a better mechanism)

## Must-Know
- Plugin data dir changes based on load method: `todoist-sync` (manual), `todoist-sync-inline` (`--plugin-dir`), `todoist-sync-ab-stack` (marketplace install). Config must exist in whichever one is active.
- `additionalContext` in SessionStart hooks is a hint the model can ignore. The reliable path for task fetching is `/todoist-sync:todoist-sync` which loads the SKILL.md.
- Stop hooks only accept top-level JSON fields: `decision`, `systemMessage`, `reason`, `continue`, `suppressOutput`. NOT `hookSpecificOutput`.
- SessionStart hooks DO accept `hookSpecificOutput.additionalContext` — and `systemMessage` shows in the transcript.
- ralph-loop has a permission error on its stop hook — unrelated to todoist-sync, ignore it.
- Todoist labels already exist: quick-win (2183384733), blocked (2183384732), needs-design (2183384734).
- ab-stack repo: `aryanbhats/ab-stack` on GitHub. Latest commit: `2af19c6`.
- Memory file updated at `~/.claude/projects/-Users-aryanbhatia-Documents-0DevProjects/memory/todoist_dev_tracking.md`.
