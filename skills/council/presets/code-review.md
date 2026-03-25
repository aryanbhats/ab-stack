---
name: Code Review Council
invoke: code
agent_count: 5
judge_mode: assistant
persona_style: functional-role
---

## Gallery Personas
- gallery/code/security.md
- gallery/code/performance.md
- gallery/code/correctness.md
- gallery/code/maintainability.md
- gallery/common/devils-advocate.md

## Consensus Rules
Severity x agreement scoring. An issue flagged by 3+ personas at high severity = Critical. An issue flagged by 2 personas or at medium severity = Warning. Single-persona low-severity findings = Suggestion. The judge synthesizes across all analyses with independent judgment — agreement amplifies signal but does not replace reasoning.

## Output Format
VERDICT: Approve / Revise / Reject

CRITICAL: [must fix before merge]
- [file:line] Issue description (flagged by N/5 reviewers)

WARNINGS: [should fix, not blocking]
- ...

SUGGESTIONS: [optional improvements]
- ...

DISSENTING VIEW: [strongest argument that this code has problems]

## Auto-Suggest Triggers
- After significant code changes
- Before creating a PR
- When user says "review this"
