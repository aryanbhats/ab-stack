# Council — Test Prompts

Run these to verify the skill works across all presets.

---

## Finance

```
/council finance "NVDA is trading at 130 with a forward P/E of 30x and projected 40% revenue growth from data center AI demand. The stock has pulled back 15% from highs. Should I initiate a position, and if so, what size relative to a $50K portfolio?"
```

Verify: 5 personas, Risk Manager constrains sizing, BUY/HOLD/SELL + conviction, user-as-judge.

## Code Review

```
/council code
```

(Picks up recent git diff. Or specify a file to review.)

Verify: Tiered issues (Critical/Warning/Suggestion), severity x agreement scoring, assistant-as-judge.

## Planning

```
/council planning "I want to build a Flask app that manages content across 5 social platforms with a kanban board, API integrations for auto-posting, and an analytics dashboard. Is this the right architecture or am I over-engineering?"
```

Verify: Architect vs. Pragmatist tension, user-as-judge, Proceed/Revise/Rethink output.

## Content

```
/council content "Here's a draft reel script: 'POV: You just discovered that Claude can read your entire codebase. Here's what I built in 30 minutes that would've taken a team 2 weeks.' — Is this going to perform? What's missing?"
```

Verify: 5 dimension scores (Brand, SEO, Audience, Conversion, Growth), platform-specific notes, user-as-judge.

## Business

```
/council business "I'm a grad student with several AI tools I've built. Should I try to turn one into a startup after graduation, join a big tech company for 2-3 years first, or stay at my current employer and build on the side?"
```

Verify: C-suite personas, CFO flags financial constraints, user-as-judge, Proceed/Pivot/Hold/Kill.

## Research

```
/council research "I'm using a multi-agent debate framework to improve investment decision quality. My hypothesis is that multi-persona deliberation improves accuracy by 10-15% over single-perspective analysis. Is this methodology sound? What baselines am I missing?"
```

Verify: Baseline Scout finds missing comparisons, diversity scoring, assistant-as-judge, Accept/Reject + scores.

## General

```
/council "I have 15 side projects in various states of completion. I can realistically maintain 3-4. What criteria should I use to decide what to keep, archive, or kill?"
```

Verify: Default 5 personas, assistant-as-judge, Decision + Reasoning + Dissent + Caveats.

## Deep Mode

```
/council --deep "Should I open-source a personal AI skill system with novel techniques? It could build reputation but means maintaining docs for strangers and potentially enabling competitors."
```

Verify: Phase 0 meta-deliberation designs a bespoke council (not just general preset), custom personas with built-in tension, then normal flow runs.

---

## Quick Checklist

After any test:

- [ ] Personas were adapted to the question (not gallery defaults copied verbatim)
- [ ] Each persona gave ONE specific suggestion
- [ ] Outputs were anonymized before judge synthesis
- [ ] Judge mode matched the preset
- [ ] Output format matched the domain template
- [ ] Proceedings saved as .md file
- [ ] At least two personas genuinely disagreed
