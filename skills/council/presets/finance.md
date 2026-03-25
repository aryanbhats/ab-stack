---
name: Finance Investment Council
invoke: finance
agent_count: 5
judge_mode: user
persona_style: famous-figure
---

## Gallery Personas
- gallery/finance/value-investor.md
- gallery/finance/growth-investor.md
- gallery/finance/contrarian.md
- gallery/finance/macro-analyst.md
- gallery/finance/risk-manager.md

## Consensus Rules
Risk Manager has VETO power on position sizing — no position can exceed Risk Manager's recommended maximum regardless of other personas' conviction. 3/5 agreement required for BUY or SELL verdict; otherwise default to HOLD. Conviction score reflects degree of agreement (5 = unanimous, 1 = bare majority). The user acts as final judge and can override any recommendation.

## Output Format
VERDICT: BUY / HOLD / SELL
CONVICTION: [1-5 based on persona agreement]
POSITION SIZE: [% of portfolio, constrained by Risk Manager]

BULL CASE: [strongest argument for]
BEAR CASE: [strongest argument against]
RISK FACTORS: [what could invalidate this thesis]
KEY METRICS: [numbers that matter for this decision]

INDIVIDUAL ANALYSES: [collapsed section with each persona's full take]

## Auto-Suggest Triggers
- When stocks, tickers, or investment decisions are mentioned
- When evaluating a potential investment or trade
- When reviewing portfolio allocation
