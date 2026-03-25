# ab-stack

Skills for AI coding agents. Each skill lives in `skills/<name>/` with a `SKILL.md` entry point.

## Structure

- `skills/` — One directory per skill. Each has a `SKILL.md` that Claude Code loads on invocation.
- `demos/` — Real proceedings from council sessions. Evidence, not fabricated examples.
- `references/` within skills — Design principles, output formats, research backing.
- `gallery/` within council — 44 persona templates across 7 domains.

## Testing

Invoke skills with test prompts from `skills/<name>/TESTING.md`.

## Adding Skills

See `CONTRIBUTING.md`. New skills go in `skills/<name>/SKILL.md`.
