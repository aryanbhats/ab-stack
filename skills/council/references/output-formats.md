# Output Formats by Domain

Each domain has a structured output template for the judge synthesis (Phase 6) and the proceedings document (Phase 7). The judge MUST use the template for their domain — this ensures consistency and actionability.

---

## General

**Judge mode:** Assistant-as-Judge

```markdown
## Council Decision

**Question:** [Original question]
**Decision:** [Clear, unambiguous statement]

### Reasoning
[2-3 paragraphs explaining the decision. Which arguments were most compelling and why. What tradeoffs were accepted.]

### Compelling Arguments
- [Argument 1 — from Analysis X]
- [Argument 2 — from Analysis Y]

### Overruled Dissent
- **[Analysis Z]**: [Their position] — Overruled because: [specific reason]

### Caveats
- [Condition that could reverse this decision]
- [Open question that needs monitoring]

### Persona Reveal
- Analysis A → [Persona Name/Role]
- Analysis B → [Persona Name/Role]
- ...
```

---

## Planning

**Judge mode:** User-as-Judge

```markdown
## Council Review: [Plan Name]

**Recommendation:** Proceed / Revise / Rethink

### Key Concerns
1. [Concern] — raised by Analysis [X]
2. [Concern] — raised by Analysis [Y]

### Blind Spots Identified
- [Something the plan doesn't account for]
- [Assumption that needs validation]

### Recommended Changes
1. [Specific change with rationale]
2. [Specific change with rationale]

### Dissenting View
**[Analysis Z]** argues: [their position and why it matters even if overruled]

### Persona Reveal
- Analysis A → [Persona Name/Role]
- ...
```

---

## Code

**Judge mode:** Assistant-as-Judge

```markdown
## Council Code Review

**Verdict:** Approve / Revise / Reject

### Critical (must fix before merge)
- [ ] `file:line` — [Issue description] — raised by Analysis [X]

### Warning (should fix, non-blocking)
- [ ] `file:line` — [Issue description] — raised by Analysis [X]

### Suggestion (consider for improvement)
- [ ] `file:line` — [Issue description] — raised by Analysis [X]

### Consensus Points
[Issues raised by 2+ analyses — these have the highest signal]

### Dissenting View
**[Analysis Z]** flagged: [their concern and why it was deprioritized]

### Persona Reveal
- Analysis A → [Persona Name/Role]
- ...
```

---

## Finance

**Judge mode:** User-as-Judge

```markdown
## Council Analysis: [Asset/Position]

**Signal:** BUY / HOLD / SELL
**Conviction:** [1-5] (1=low confidence, 5=high confidence)
**Position Size:** [Suggested allocation as % or dollar amount, if applicable]

### Bull Case
[Strongest argument for the long position — from Analysis X]

### Bear Case
[Strongest argument against — from Analysis Y]

### Risk Factors
1. [Risk] — severity: High/Medium/Low
2. [Risk] — severity: High/Medium/Low

### Key Disagreement
[The core tension between analyses — what the user must resolve]

### Persona Reveal
- Analysis A → [Persona Name/Role]
- ...

---
*This is deliberation output, not financial advice. The user makes all investment decisions.*
```

---

## Content

**Judge mode:** User-as-Judge

```markdown
## Council Review: [Content Piece Title]

**Recommendation:** Publish / Revise / Rethink

### Dimension Scores
| Dimension | Score (1-10) | Notes |
|-----------|:---:|-------|
| Brand Alignment | X | [Brief note] |
| SEO Potential | X | [Brief note] |
| Audience Resonance | X | [Brief note] |
| Conversion Potential | X | [Brief note] |
| Growth/Shareability | X | [Brief note] |

### Top Changes (ranked by impact)
1. [Specific change] — impacts [dimension]
2. [Specific change] — impacts [dimension]
3. [Specific change] — impacts [dimension]

### Platform-Specific Notes
- **[Platform 1]:** [Adaptation needed]
- **[Platform 2]:** [Adaptation needed]

### Dissenting View
**[Analysis Z]** argues: [their position on what matters most]

### Persona Reveal
- Analysis A → [Persona Name/Role]
- ...
```

---

## Business

**Judge mode:** User-as-Judge

```markdown
## Council Analysis: [Decision/Proposal]

**Recommendation:** Proceed / Pivot / Hold / Kill

### Strategic Fit
[How this aligns with or conflicts with current strategy — 2-3 sentences]

### Impact Assessment
| Dimension | Rating | Notes |
|-----------|:---:|-------|
| Financial Impact | High/Med/Low | [Brief note] |
| Operational Feasibility | High/Med/Low | [Brief note] |
| Technical Feasibility | High/Med/Low | [Brief note] |
| Market Opportunity | High/Med/Low | [Brief note] |

### Blockers
1. [Blocker] — [What needs to happen to unblock]
2. [Blocker] — [What needs to happen to unblock]

### Key Tradeoffs
- [If we do X, we give up Y]
- [If we prioritize A, we delay B]

### Dissenting View
**[Analysis Z]** argues: [their position and the scenario where they'd be right]

### Persona Reveal
- Analysis A → [Persona Name/Role]
- ...
```

---

## Research

**Judge mode:** Assistant-as-Judge

```markdown
## Council Review: [Paper/Study Title]

**Verdict:** Strong Accept / Accept / Weak Accept / Weak Reject / Reject

### Scores
| Dimension | Score (1-10) |
|-----------|:---:|
| Methodology | X |
| Novelty | X |
| Statistical Rigor | X |
| Practical Impact | X |
| Completeness | X |

### Strengths
1. [Strength — from Analysis X]
2. [Strength — from Analysis Y]

### Weaknesses
1. [Weakness — from Analysis X]
2. [Weakness — from Analysis Y]

### Missing
- [What the work doesn't address that it should]
- [Data or analysis that would strengthen the claims]

### Questions for Authors
1. [Question that would clarify a key uncertainty]
2. [Question about methodology or assumptions]

### Review Diversity Check
[Note on whether reviewers covered genuinely different aspects or converged on the same points]

### Persona Reveal
- Analysis A → [Persona Name/Role]
- ...
```

---

## Proceedings Document Structure

Every council session produces a proceedings file regardless of domain. The file combines the domain-specific output above with the full deliberation record:

```markdown
# Council Proceedings: [Question Summary]

**Date:** YYYY-MM-DD HH:MM
**Preset:** [domain]
**Judge Mode:** Assistant-as-Judge / User-as-Judge
**Personas:** [count]

## Question
[Full question text]

## Context Summary
[Brief summary of context provided to all personas]

## Deliberation

### [Persona 1 Name/Role]
[Full analysis output]

### [Persona 2 Name/Role]
[Full analysis output]

...

## Synthesis
[Domain-specific output template from above]

## Key Tensions
1. [Tension between Persona X and Persona Y — how it was resolved]
2. [Tension — resolution]

## Open Questions
- [Question that remains unresolved]
- [Question for future consideration]
```
