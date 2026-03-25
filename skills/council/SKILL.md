---
name: council
description: "Convene a council of expert personas for multi-perspective deliberation. Use when facing non-trivial decisions across any domain: architecture, investments, content strategy, code review, business strategy, research. Invoke as /council [preset] where preset is one of: general, planning, code, finance, content, business, research. Add --deep for novel questions that need a bespoke council."
---

# /council — Multi-Persona Deliberation Skill

## Invocation

```
/council [preset] "question"
/council --deep [preset] "question"
```

**Presets:** `general` (default), `planning`, `code`, `finance`, `content`, `business`, `research`

If no preset is specified, use `general`. If an unknown preset is given, fall back to `general` and note it.

## Auto-Suggest Triggers

Proactively suggest `/council` when you detect:
- Architecture decisions with multiple valid approaches
- Financial or investment questions with real capital at stake
- Content strategy or branding decisions
- Code review where you're genuinely uncertain about the best pattern
- Business strategy with competing priorities
- Any moment where you catch yourself hedging between 2+ substantive options

## Core Principle: Dynamic Persona Generation

Gallery personas in `presets/` are **examples and a quality floor**, not rigid configs. For every council invocation, Claude ADAPTS or GENERATES personas tailored to the specific question. The gallery shows what a great persona looks like — the right level of specificity, the right format, the right tension. Claude then creates personas that serve THIS question.

## The --deep Flag

When `--deep` is passed, read `references/deep-mode.md` and run Phase 0 (meta-deliberation) before the normal flow. Use for novel questions that don't fit existing domains, cross-domain questions, or high-stakes decisions worth the extra compute.

---

## 7-Phase Orchestration Flow

### Phase 1: INTAKE

Parse the invocation to extract:
- **Preset**: Which domain (default: `general`)
- **Question**: The deliberation topic
- **Flags**: `--deep` for meta-deliberation

If `--deep` is set, read `references/deep-mode.md` and execute Phase 0 before continuing.

Load the preset file from `presets/{preset}.md` if it exists. If the preset file is missing, proceed with general-domain defaults. Read `references/output-formats.md` to load the output template for this domain.

### Phase 2: CONTEXT GATHERING

Assemble the material all personas will analyze. Depending on the question type:

- **Code questions**: Read relevant source files, `git diff`, test results, error logs
- **Architecture questions**: Read project structure, existing patterns, dependencies
- **Finance questions**: Gather the asset/position details, any research context the user provided
- **Content questions**: Read the draft, brand guidelines, target audience info
- **Business questions**: Read the proposal, financial projections, market context
- **Planning questions**: Read the plan document, timeline, resource constraints
- **Research questions**: Read the paper/methodology, data, prior work

Package this as a **context block** that every persona receives identically. If context is very large (>50KB), summarize the key points and include file paths for agents to read directly.

### Phase 3: PERSONA GENERATION

1. Read the preset file to understand the domain and any gallery personas.
2. Read `references/persona-design.md` for design principles.
3. Read gallery persona files for this domain as EXAMPLES of quality.
4. **ADAPT or GENERATE 3-5 personas** tailored to this specific question.

Each persona MUST have:
- **Name/Role**: A named professional (creative/strategic) or functional role (technical)
- **Evaluation Lens**: The specific angle they analyze through
- **Priorities**: What they optimize for (ranked)
- **Blind Spots**: What they systematically underweight
- **ONE-IDEA RULE**: Each persona delivers ONE specific, actionable suggestion — concrete enough to implement. Not rambling analysis. One idea, well-argued.

Critical design rules:
- At least one persona must be a **structural contrarian** (Devil's Advocate)
- Personas must have **genuine tension** with each other (e.g., Pragmatist vs Security Expert, Growth vs Sustainability)
- 5 personas is optimal for most questions; use 3 for narrow questions, 4-5 for complex ones
- Each persona must evaluate through genuinely different criteria, not just different labels on the same thinking

### Phase 4: PARALLEL DELIBERATION

Spawn each persona as a background agent using `run_in_background: true`.

Each agent receives:
1. Their persona prompt (lens, priorities, blind spots, output rules)
2. The full context block from Phase 2
3. The ONE-IDEA RULE: "You must deliver ONE specific, actionable suggestion through your lens. Be concrete enough that someone could implement your suggestion without asking clarifying questions. Do not hedge or list multiple options."

Wait for all agents to complete. **If an agent fails or times out, proceed with N-1 agents and note the gap in the proceedings.** Do not retry — the council can function with 2+ perspectives.

### Phase 5: ANONYMIZATION

Strip all persona labels from the outputs. Present them as:
- **Analysis A**, **Analysis B**, **Analysis C**, etc.

This prevents anchoring bias during judgment. The judge evaluates arguments on merit, not authority. Persona labels are revealed AFTER the decision is made.

### Phase 6: JUDGE SYNTHESIS

Two modes, configured per preset:

#### Mode 1: Assistant-as-Judge (code, general, research)

The assistant reviews all anonymized analyses and exercises **independent judgment** — this is NOT vote counting or majority rule. The assistant:

1. Names the decision clearly
2. Identifies the most compelling arguments (regardless of which "won")
3. Names any overruled dissent and explains WHY it was overruled
4. Lists caveats and conditions that could reverse the decision
5. Reveals persona labels after the decision

Read `references/output-formats.md` for the domain-specific output template.

#### Mode 2: User-as-Judge (finance, content, business, planning)

Present all anonymized analyses to the user in a structured format. The user reads, deliberates, and makes the call. The assistant:

1. Presents each analysis clearly with its one key suggestion
2. Highlights points of tension between analyses
3. Asks the user for their decision
4. Structures the user's decision into the domain-specific output format
5. Reveals persona labels after the user decides

### Phase 7: DOCUMENTATION

Save the full proceedings as a structured markdown file:

```
council-proceedings-{preset}-{YYYYMMDD-HHMMSS}.md
```

**Location logic:**
1. If a `docs/` directory exists in the project, save there
2. Otherwise, save in the current working directory

The proceedings file includes:
- Question and context summary
- Each persona's analysis (now labeled)
- The judge's synthesis or user's decision
- Key tensions and how they were resolved
- Caveats and open questions

---

## Error Handling

| Scenario | Action |
|---|---|
| Unknown preset | Fall back to `general`, note in proceedings |
| Preset file missing | Proceed with general-domain defaults |
| Agent fails/times out | Proceed with N-1 agents, note the gap |
| No context available | Ask the user to provide context before proceeding |
| Very large context (>50KB) | Summarize key points, give agents file paths |

---

## Reference Files

These files inform persona design and output quality but are NOT required to run the flow:

- `references/persona-design.md` — Evidence-based persona design principles
- `references/output-formats.md` — Domain-specific output templates
- `references/examples.md` — Worked examples from real council sessions
- `references/deep-mode.md` — Meta-deliberation logic for --deep flag
