---
name: Research Review Council
invoke: research
agent_count: 5
judge_mode: assistant
persona_style: functional-role
---

## Gallery Personas
- gallery/research/methodology.md
- gallery/research/literature-gap.md
- gallery/research/baseline-scout.md
- gallery/research/statistical-validity.md
- gallery/research/practical-applicability.md

## Consensus Rules
Diversity scoring — if all reviewers say the same thing, the panel is failing. Dissent is a feature, not a bug. The judge should flag when review diversity is low and weight the lone dissenter more heavily in those cases. A paper that gets uniform praise deserves extra skepticism. A paper that gets uniform criticism may have a misunderstood contribution.

## Output Format
OVERALL: Strong Accept / Accept / Weak Accept / Weak Reject / Reject

SCORES:
- Methodology: [1-10]
- Novelty: [1-10]
- Statistical Rigor: [1-10]
- Practical Impact: [1-10]
- Completeness: [1-10]

STRENGTHS: [what the work does well]
WEAKNESSES: [what needs improvement]
MISSING: [what's absent — baselines, citations, experiments]
QUESTIONS FOR AUTHORS: [specific questions that need answers]

REVIEW DIVERSITY: [how much reviewers disagreed — high diversity = valuable signal]

## Auto-Suggest Triggers
- When reviewing papers, research proposals, or academic work
- When evaluating experimental methodology
- When assessing statistical claims or study design
