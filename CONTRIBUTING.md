# Contributing

## Adding a New Skill

1. Create `skills/<name>/SKILL.md` — the entry point Claude reads on invocation
2. Add `skills/<name>/TESTING.md` — test prompts to verify it works
3. Add any supporting files (references, templates, etc.)
4. Run `./setup` to install locally and test
5. Open a PR

## Adding a New Council Domain

1. Create persona files in `skills/council/gallery/<domain>/`
2. Create a preset at `skills/council/presets/<domain>.md`
3. Test: `/council <domain> "test question"`

No changes to `SKILL.md` needed — the orchestration auto-discovers presets.

## Adding a Persona to an Existing Domain

1. Create a `.md` file in `skills/council/gallery/<domain>/`
2. Add it to the preset's persona list in `skills/council/presets/<domain>.md`
3. Test with a relevant question

## Persona Quality Bar

Every persona must pass these tests:

**Swap test:** If you swap two personas' names and the output wouldn't change, they're not diverse enough. Real diversity means different evaluation criteria, not different job titles.

**Tension test:** Your persona must naturally disagree with at least one other persona in the same preset. Pragmatist vs. Architect. Growth vs. Sustainability. Security vs. Speed. If everyone agrees, the council is failing.

**ONE-IDEA test:** Can you state one specific, actionable suggestion in 2-3 sentences? If your persona would need a paragraph of caveats, the lens is too broad.

**Blind spot test:** Every persona must have documented blind spots. If a persona has no blind spots, it's not specific enough.

## PR Guidelines

- Test your changes with at least one real invocation
- Include the test prompt and a summary of results
- Don't modify `SKILL.md` unless you're changing orchestration logic
- Persona files should follow the format in `ARCHITECTURE.md`
