# Deep Mode: Meta-Deliberation

When `/council --deep "question"` is invoked, run Phase 0 before the normal 7-phase flow. Phase 0 designs a bespoke council for THIS specific question rather than using preset defaults.

---

## When to Use --deep

- **Novel questions** that don't fit cleanly into any existing preset domain
- **Cross-domain questions** that span multiple areas (e.g., "should we open-source our internal tool?" touches code, business, content, and community)
- **High-stakes decisions** where the extra 2-3 Claude calls for meta-deliberation are justified by the decision's impact
- **Questions where the obvious personas feel wrong** — if you read the preset and think "these personas won't capture what matters here," use --deep

Do NOT use --deep for straightforward domain questions. A code review doesn't need meta-deliberation. An investment thesis for a well-known stock doesn't need it. --deep is for when the question itself is unusual.

---

## Phase 0: Meta-Deliberation

Before spawning any council personas, Claude deliberates on the council design itself. This is a structured internal reasoning process, not a separate agent call.

### Step 1: Question Decomposition

Break the question into its constituent dimensions:

- **What type of decision is this?** (Binary choice, ranking, design, go/no-go, resource allocation, strategy)
- **What domains does it touch?** (Technical, financial, creative, organizational, ethical, legal)
- **What's at stake?** (Reversibility, capital, reputation, time, relationships)
- **Who are the stakeholders?** (Direct, indirect, future)
- **What's the time horizon?** (Days, months, years)
- **What information is available vs. missing?**

### Step 2: Perspective Design

Based on the decomposition, design the evaluation axes:

Ask: "What are the 3-5 genuinely different ways a thoughtful person could evaluate this decision?"

For each axis:
- What does this perspective optimize for?
- What does it systematically underweight?
- What's its natural tension with the other axes?

Validate: Do any two axes collapse into the same evaluation when applied to THIS question? If yes, merge them and find a genuinely different axis.

### Step 3: Council Specification

Design the full council:

```
COUNCIL SPECIFICATION
=====================
Question: [restated clearly]
Decision Type: [from Step 1]
Domains: [from Step 1]
Stakes: [from Step 1]

Persona Count: [3-5, justified]

Persona 1:
  Style: Named Professional / Functional Role / Historical Figure
  Name: [name]
  Lens: [evaluation axis]
  Priorities: [ranked]
  Blind Spots: [what they miss]
  Tension With: [which other persona(s) they'll disagree with]

Persona 2: ...
Persona 3: ...
[etc.]

Contrarian: Persona [N] serves as structural contrarian

Judge Mode: Assistant-as-Judge / User-as-Judge
  Rationale: [why this mode fits]

Output Format: [which domain template to use, or custom]
  If custom, define the template structure here.

Consensus Mechanism:
  [How disagreements are resolved — majority doesn't rule,
   argument quality does. Note any domain-specific weighting.]
```

### Step 4: Sanity Check

Before proceeding, validate the design:

1. **Diversity check:** Would swapping any two personas' names change their output? If not, they're not diverse enough.
2. **Tension check:** Are there at least 2 pairs of personas with natural disagreements on this question?
3. **Coverage check:** Is there a plausible important perspective that none of the personas would raise? If yes, add it or merge it into the closest persona.
4. **Contrarian check:** Does the contrarian have a genuine, defensible position — or are they just saying "what if it fails?" A good contrarian proposes an alternative, not just opposition.
5. **Actionability check:** Will each persona's ONE-IDEA RULE output be implementable for this type of question? If the question is abstract (e.g., "what should our values be?"), adjust the output expectation to be specific enough to act on.

If any check fails, revise the specification before proceeding to Phase 1.

---

## Example: Cross-Domain Deep Mode

**Question:** "Should we open-source our internal deployment tool?"

### Step 1: Decomposition
- Decision type: Go/no-go with conditions
- Domains: Technical (code quality, maintenance), Business (competitive advantage, hiring), Legal (licensing, IP), Community (adoption, contribution)
- Stakes: Irreversible (once public, always public), moderate (not core product)
- Time horizon: Years (maintenance commitment)

### Step 2: Perspective Design
1. **Competitive Moat axis:** Does open-sourcing strengthen or weaken our position?
2. **Engineering Cost axis:** What's the true maintenance burden of a public repo?
3. **Talent Acquisition axis:** Does this help us hire better engineers?
4. **Legal/IP axis:** What are the licensing and liability implications?
5. **Community axis:** Will anyone actually use and contribute to this?

### Step 3: Specification
- 5 personas, mixed style (2 named professionals, 3 functional roles)
- Contrarian: The Engineering Cost persona (argues against the feel-good "open source everything" default)
- Judge: User-as-Judge (business decision with values component)
- Output: Business template with custom "Open Source Readiness" section
- Tensions: Competitive Moat vs. Talent Acquisition, Engineering Cost vs. Community

### Step 4: Sanity Check
- Diversity: All 5 evaluate through genuinely different criteria. Pass.
- Tension: 2+ pairs identified. Pass.
- Coverage: Missing "existing user impact" — merged into Community persona. Pass.
- Contrarian: Engineering Cost will argue specific maintenance hour estimates, not just "it's risky." Pass.
- Actionability: Each persona can give one concrete recommendation (license choice, code audit scope, community strategy, etc.). Pass.

Proceed to Phase 1 with this specification.

---

## Deep Mode Adds ~2 Minutes

Phase 0 typically adds 2-3 minutes to the council process. This is justified when:
- The question is worth more than 3 minutes of deliberation
- The standard presets would produce mediocre personas for this question
- The user explicitly requested --deep

It is NOT justified for routine decisions within a well-defined domain. Trust the presets for those.
