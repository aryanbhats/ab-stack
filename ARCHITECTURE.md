# Architecture

## Skill Structure

Each skill lives in `skills/<name>/` with `SKILL.md` as the entry point. Claude Code reads `SKILL.md` when the skill is invoked — it's self-contained orchestration instructions.

```
skills/<name>/
├── SKILL.md           # Entry point — Claude reads this on invocation
├── TESTING.md         # Test prompts to verify the skill works
├── references/        # Design principles, research, output templates
├── gallery/           # Persona/template files (council-specific)
└── presets/           # Configuration files for different modes
```

Skills are pure markdown. No build step, no compiled binaries, no runtime dependencies.

## Council: Design Decisions

### Why Dynamic Personas, Not a Lookup Table

Gallery personas are quality examples, not rigid assignments. For every question, Claude adapts or generates personas tailored to the specific context. A "Value Investor" becomes a "Semiconductor Value Analyst" when the question is about NVDA.

This beats a fixed registry because the persona's lens gets sharpened for the actual question.

### Why Anonymization

From Karpathy's LLM-as-Judge work: when "Senior Architect" and "Junior Developer" give the same suggestion, judges rate the architect's higher. Anonymization forces evaluation on argument merit.

Labels are revealed after the decision — you still see who argued what, but the judgment wasn't influenced by reputation.

### Why the ONE-IDEA Rule

From a real council session: five experts each gave one concrete suggestion. The winner was a single CSS rule ("4px accent stripe") that beat an ambitious "verdict box" system — because it was implementable in five minutes.

Forcing one idea per persona eliminates hedge-stacking and generic observations. Each persona commits to their best insight.

### Why Two Judge Modes

For technical decisions (code review, research evaluation), the assistant has enough domain knowledge to synthesize. For strategic, creative, and financial decisions, the user should judge — the assistant doesn't have the user's values, risk tolerance, or context.

### Why 5 Personas (Not 3 or 7)

Research shows 5 consistently outperforms 3 (insufficient diversity) and 7-10 (diminishing returns, increased peer pressure risk). Five is the sweet spot.

## Persona File Format

```markdown
---
name: "Role Name"
title: "Description — Professional Frame"
style: famous-figure | named-professional | functional-role
---

## Evaluation Lens
What this persona uniquely looks at.

## Priorities
1. What they optimize for above all
2. Second priority
3. Third priority

## Blind Spots
- What they systematically underweight

## Key Questions
1. Question they always ask
2. Question they always ask
3. Question they always ask

## Output Rules
- ONE specific, actionable suggestion
- Concrete enough to implement without clarifying questions
- State what you'd do AND what it costs
- No hedging. Take a position.
```

### Three Persona Styles

| Style | When | Example |
|-------|------|---------|
| **famous-figure** | Documented philosophy provides the lens | "Buffett — intrinsic value, margin of safety" |
| **named-professional** | Creative/strategic where credentials ground advice | "Elena Torres, Head of Brand, Conde Nast" |
| **functional-role** | Technical domains where the role IS the lens | "Security Reviewer — OWASP top 10, auth bypass" |

## Preset File Format

Each preset defines: which personas to start from, judge mode (assistant or user), output format, and consensus mechanism. See `skills/council/presets/` for examples.

## Adding Skills

New skills go in `skills/<name>/SKILL.md`. The `setup` script auto-discovers and installs all skills under `skills/`. No manifest or registry needed.
