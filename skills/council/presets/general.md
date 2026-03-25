---
name: General Council
invoke: general
agent_count: 5
judge_mode: assistant
persona_style: functional-role
---

## Gallery Personas
- gallery/common/skeptic.md
- gallery/common/pragmatist.md
- gallery/common/innovator.md
- gallery/common/risk-analyst.md
- gallery/common/devils-advocate.md

## Consensus Rules
Judge exercises independent judgment. Not vote counting. Identify where analyses agree (high confidence) and disagree (requires judgment). Override the majority if the dissenting argument is stronger.

## Output Format
DECISION: [What the judge decided]
REASONING: [Why — citing which analyses were most compelling]
DISSENT: [Strongest argument against this decision, and why it was overruled]
CAVEATS: [Conditions or risks to monitor]

## Auto-Suggest Triggers
- Binary decisions with significant consequences
- When Claude is uncertain about the best approach
- Situations where the user is weighing tradeoffs
