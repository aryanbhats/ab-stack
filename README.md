# ab-stack

Skills for AI coding agents. Start with `/council`.

Instead of asking one AI for advice, convene a **board of directors**, **investment committee**, **code review panel**, or **research council** — each member genuinely independent, each bringing a distinct evaluation lens, each forced to give **one specific actionable suggestion**. Then a judge synthesizes the decision with all arguments anonymized.

## `/council` — Multi-Persona Deliberation

```
/council finance "Should I buy NVDA at current levels?"
/council code                    # reviews your recent changes
/council planning                # challenges the current plan
/council --deep "Should we pivot to B2B?"
```

### How It Works

```
                           /council [preset] "question"
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                   │
              ┌─────▼─────┐   ┌──────▼──────┐   ┌───────▼───────┐
              │ Persona A  │   │  Persona B   │   │  Persona C    │
              │ (Security) │   │ (Performance)│   │ (Devil's Adv) │
              │            │   │              │   │               │
              │ ONE idea   │   │  ONE idea    │   │  ONE idea     │
              └─────┬──────┘   └──────┬───────┘   └───────┬───────┘
                    │                 │                     │
                    │    all run in parallel, independent   │
                    │    no shared context, no anchoring    │
                    └─────────────────┼─────────────────────┘
                                      │
                              ┌───────▼────────┐
                              │  ANONYMIZATION  │
                              │                 │
                              │ Strip labels →  │
                              │ "Analysis A"    │
                              │ "Analysis B"    │
                              │ "Analysis C"    │
                              └───────┬─────────┘
                                      │
                              ┌───────▼────────┐
                              │     JUDGE       │
                              │                 │
                              │ Assistant mode: │
                              │  synthesizes    │
                              │                 │
                              │ User mode:      │
                              │  YOU decide     │
                              └───────┬─────────┘
                                      │
                              ┌───────▼────────┐
                              │ SAVE PROCEEDINGS│
                              │ (.md file)      │
                              └────────────────┘
```

### Quick Start

```bash
# Clone
git clone https://github.com/aryanbhats/ab-stack.git

# Install (symlinks skills to ~/.agents/skills/)
cd ab-stack && ./setup

# Use
/council "your question here"
```

### 7 Presets

| Preset | Invoke | Judge | Personas | Output |
|--------|--------|-------|----------|--------|
| **General** | `/council` | Assistant | Skeptic, Pragmatist, Innovator, Risk Analyst, Devil's Advocate | Decision + reasoning + dissent |
| **Planning** | `/council planning` | User | Architect, Pragmatist, Skeptic, User Advocate, Devil's Advocate | Proceed / Revise / Rethink |
| **Code Review** | `/council code` | Assistant | Security, Performance, Correctness, Maintainability, Devil's Advocate | Approve / Revise / Reject (tiered) |
| **Finance** | `/council finance` | User | Value Investor, Growth Investor, Contrarian, Macro Analyst, Risk Manager | BUY / HOLD / SELL + conviction |
| **Content** | `/council content` | User | Brand Guardian, SEO, Audience Resonance, Conversion, Growth | Publish / Revise / Rethink + scores |
| **Business** | `/council business` | User | CEO, CFO, COO, CTO, CMO | Proceed / Pivot / Hold / Kill |
| **Research** | `/council research` | Assistant | Methodology, Literature Gap, Baseline Scout, Statistics, Applicability | Accept → Reject + scores |

### The ONE-IDEA Rule

The core principle. Each persona delivers **one** specific, actionable suggestion — not a list, not a ramble, not hedged advice.

```
BAD (generic, hedging):
"There are several security concerns to consider. You might want to
 look at input validation, and it could be worth checking the auth
 flow. Also, error messages might leak information."

GOOD (one idea, concrete):
"The OAuth callback at auth.py:47 accepts a redirect_uri parameter
 from the query string without validating it against an allowlist.
 An attacker can craft a URL that redirects the auth code to their
 server. Fix: add ALLOWED_REDIRECT_URIS to config and validate
 before redirecting. Cost: 15 minutes, 8 lines of code."
```

This came from a real council session where Sarah's "4px navy accent stripe" beat Marcus's ambitious "verdict box" — because it was one CSS rule that could ship in five minutes.

### Anonymization

Strips persona labels before the judge sees the arguments. Prevents weighting advice by reputation.

```
WITHOUT anonymization:                WITH anonymization:
┌─────────────────────────┐           ┌─────────────────────────┐
│ "Buffett says BUY"       │          │ "Analysis A says BUY"    │
│ "Burry says SELL"        │          │ "Analysis B says SELL"   │
│                          │          │                          │
│ Judge: "Well, Buffett    │          │ Judge: "Analysis B's     │
│ is usually right..."     │          │ data on short interest   │
│                          │          │ is more compelling       │
│ → Bias toward authority  │          │ because..."              │
└─────────────────────────┘           │                          │
                                      │ → Evaluated on merit     │
                                      └─────────────────────────┘
```

Labels are revealed **after** the decision so you can see who argued what — but the judgment wasn't biased by reputation.

### Dynamic Persona Generation

Gallery personas are **examples, not assignments**. For every invocation, Claude reads the gallery to understand the quality bar, then adapts or generates personas tailored to THIS specific question.

```
Gallery Persona (example)              What Claude Actually Creates
┌─────────────────────────┐            ┌──────────────────────────────┐
│ Value Investor           │    →      │ Semiconductor Value Analyst   │
│ Buffett/Graham           │  adapts   │ Buffett lens applied to chip  │
│ Generic intrinsic value  │    to     │ cyclicality + fab capex       │
└─────────────────────────┘  question  └──────────────────────────────┘
```

### Deep Mode

For questions that don't fit existing presets. `--deep` adds a meta-deliberation phase that designs a bespoke council before running it.

```
/council --deep "Should we open-source our internal tool?"
```

Claude first asks: "What kind of council does THIS question need?" — decomposing the decision type, identifying evaluation axes, building custom personas with built-in tension, and sanity-checking for diversity before running the deliberation.

Costs ~2-3 extra Claude calls. Use when the question is worth it.

### Judge Modes

| Mode | Used For | How It Works |
|------|----------|--------------|
| **Assistant-as-Judge** | Code, General, Research | Assistant exercises independent judgment — not vote counting. Quality of argument wins. |
| **User-as-Judge** | Finance, Content, Business, Planning | All anonymized analyses presented to you. You read, deliberate, decide. Assistant structures the output. |

For creative, strategic, and financial decisions — **you** should be the judge. The assistant doesn't have your values, risk tolerance, or domain expertise.

### Consensus Mechanisms

Each domain handles disagreement differently:

- **General** — Judge evaluates argument quality (not vote counting)
- **Code Review** — Severity x agreement scoring (3+/5 at HIGH = Critical)
- **Finance** — Risk Manager has VETO on position sizing; 3/5 for BUY/SELL, else HOLD
- **Content** — Priority chain: accuracy > brand > audience > conversion > growth
- **Business** — C-suite hierarchy; CFO/Legal can flag blockers; user resolves
- **Research** — Diversity scoring; if all reviewers agree, the panel is failing

## Evidence

| Technique | Improvement | Source |
|-----------|------------|--------|
| Single-model multi-persona deliberation | **+9-13%** over CoT | Town Hall Debate Prompting, 2025 |
| Adversarial critique | **+23%** factual accuracy | MDPI Applied Sciences, 2025 |
| Persona-based evaluation, same model | **+6.2%** accuracy | ChatEval, ICLR 2024 |
| Domain-specific agents vs generic | **+10-15%** accuracy | PartnerMAS, 2025 |
| Anonymization prevents sycophantic agreement | Key design insight | Karpathy llm-council (15.9k stars) |

### Honest Caveats

- Same-model with **identical** prompts shows zero benefit — diversity must be genuine
- Multi-agent debate can transform correct answers into **incorrect** ones via peer pressure
- Simple self-consistency (ask 3 times, take majority) is the real baseline to beat
- Cost: 3-5 extra Claude calls per council — reserve for decisions that matter
- Stronger models benefit more from this technique

## 44 Personas Across 7 Domains

```
gallery/
├── common/     Skeptic, Pragmatist, Innovator, Risk Analyst, Devil's Advocate
├── finance/    Value Investor, Growth Investor, Contrarian, Macro Analyst, Risk Manager
├── code/       Security, Performance, Correctness, Maintainability
├── content/    Brand Guardian, SEO, Audience Resonance, Conversion, Growth
├── business/   CEO, CFO, COO, CTO, CMO
├── planning/   Architect, User Advocate, Maintainability Advocate
└── research/   Methodology, Literature Gap, Baseline Scout, Statistics, Applicability
```

Each persona has: evaluation lens, ranked priorities, blind spots, key questions, and the ONE-IDEA output rule.

## Extending

### Add a new domain

```
1. Create persona files in gallery/your-domain/
2. Create a preset in presets/your-domain.md
3. Use it: /council your-domain "question"

No changes to SKILL.md needed.
```

### Add a persona

```
1. Drop a .md file in gallery/[domain]/
2. Add it to the preset's persona list
3. Done
```

### Mix and match

```
/council --personas="gallery/finance/value-investor.md,gallery/code/security.md"
```

## Install

**Option 1: Clone + setup**
```bash
git clone https://github.com/aryanbhats/ab-stack.git
cd ab-stack && ./setup
```

**Option 2: Project-local**
```bash
git clone https://github.com/aryanbhats/ab-stack.git
cd ab-stack && ./setup --local
```

**Option 3: Manual**
```bash
git clone https://github.com/aryanbhats/ab-stack.git ~/.agents/skills/ab-stack
ln -s ~/.agents/skills/ab-stack/skills/council ~/.agents/skills/council
```

## Coming Soon

More skills are in development. ab-stack is a growing collection — council is the first.

## Origin

Built from analysis of 30+ repos, 15+ academic papers, and real council sessions. The ONE-IDEA rule came from an Asset Management RAG Pipeline council where five named professionals (Goldman VP, Bloomberg designer, Pentagram creative director, Two Sigma quant, portfolio manager) each gave one concrete design suggestion. The simplest one won.

## License

MIT — do whatever you want with it.
