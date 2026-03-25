# Persona Design Principles

Evidence-based guidelines for creating council personas that produce genuinely diverse, high-quality deliberation.

---

## 1. Genuine Evaluation Criteria Diversity

**Source:** ChatEval framework — +6.2% correlation with human judgment when evaluators use genuinely different criteria vs. same-criteria-different-names.

The most common failure mode is creating personas that LOOK different but THINK the same. "The Security Expert" and "The Reliability Engineer" often produce near-identical analysis. Real diversity means different **evaluation criteria**, not different job titles.

Test: If you swapped two personas' names and the output wouldn't change, your personas aren't diverse enough.

**Good diversity:** Pragmatist (cost, speed, simplicity) vs. Security Expert (attack surface, data exposure, compliance) vs. Growth Engineer (scalability, extensibility, iteration speed)

**Bad diversity:** Senior Backend Engineer vs. Staff Backend Engineer vs. Principal Backend Engineer

## 2. Always Include a Structural Contrarian

**Source:** DEBATE paper, ACL 2024 — structured opposition improves decision quality even when the contrarian position doesn't win.

Every council needs at least one persona whose job is to find problems, challenge assumptions, and argue the unpopular position. This is NOT about being negative — it's about stress-testing the group's thinking.

The contrarian should be designed to challenge the specific assumptions most likely to go unquestioned in this domain. A finance contrarian challenges bull cases. A code contrarian challenges "it works" with "but will it scale?"

## 3. ONE Specific Actionable Suggestion Per Persona

**Source:** Asset Management RAG Pipeline Financial Report Design Council — the breakthrough insight that transformed council quality.

Each persona delivers exactly ONE specific, actionable suggestion through their evaluation lens. Not a rambling analysis. Not a list of observations. One concrete idea that could be implemented without asking clarifying questions.

**Good:** "Add a 4px accent stripe in brand blue (#0055A4) to the left edge of each recommendation box — it creates visual hierarchy without adding information density."

**Bad:** "The visual design could be improved in several ways. Consider color, typography, and spacing improvements to enhance readability and professional appearance."

The ONE-IDEA RULE forces each persona to commit to their best insight rather than hedging across multiple weak observations.

## 4. Anonymize Before Judging

**Source:** Karpathy's LLM-as-Judge framework (15.9K GitHub stars) — anonymization eliminates authority bias and position bias in evaluation.

When a "Senior Architect" and a "Junior Developer" give the same suggestion, judges rate the architect's higher. Anonymization forces evaluation on merit. Present analyses as "Analysis A", "Analysis B", etc. Reveal labels only after the decision.

Also eliminates position bias — judges tend to favor the first or last analysis they read. Randomize presentation order.

## 5. Frame Around Decision Criteria, Not Expertise Titles

Design personas by WHAT THEY OPTIMIZE FOR, not what their LinkedIn says.

Start with: "What are the 3-5 genuinely different ways to evaluate this decision?" Then build a persona around each evaluation axis.

For an architecture decision:
- Axis 1: Minimize time-to-ship → The Pragmatist
- Axis 2: Minimize attack surface → The Security Auditor
- Axis 3: Maximize extensibility → The Platform Thinker
- Axis 4: Minimize operational burden → The On-Call Engineer
- Axis 5: Challenge all assumptions → The Devil's Advocate

## 6. Five Personas Is Optimal

**Source:** THDP (Tree of Heterogeneous Debate Personas) research — 5 personas consistently outperforms 3, 7, or 10 across decision quality metrics.

- 3 personas: Too few perspectives, misses blind spots. Use only for narrow, well-defined questions.
- 5 personas: Optimal diversity-to-coherence ratio. Enough tension without cacophony.
- 7+ personas: Diminishing returns. Redundant perspectives emerge. Judge synthesis becomes noisy.

Default to 5. Use 3-4 for narrow questions. Never exceed 5 unless `--deep` meta-deliberation specifically calls for it.

## 7. Named Professionals vs. Functional Roles

**Named professionals** (Marcus Chen, VP at Goldman Sachs) work best for:
- Creative and strategic domains (content, design, business)
- Finance (institutional credibility shapes analytical framing)
- Any domain where professional culture shapes the evaluation lens

**Functional roles** (The Pragmatist, The Security Auditor) work best for:
- Technical domains (code review, architecture)
- Research evaluation
- Any domain where the evaluation axis matters more than professional identity

Mix when appropriate. A code council might have functional roles plus one named "Staff Engineer at Stripe" for the production-systems perspective.

## 8. Personas Must Have TENSION With Each Other

The council's value comes from genuine disagreement, not polite consensus. Design personas whose priorities naturally conflict:

- **Pragmatist** ("ship it") vs. **Security Expert** ("lock it down")
- **Growth Strategist** ("scale fast") vs. **Sustainability Advocate** ("don't burn out")
- **User Advocate** ("simplify") vs. **Platform Thinker** ("make it extensible")
- **Quant Researcher** ("what do the numbers say") vs. **Creative Director** ("what does it feel like")

If your personas would all agree on most questions, you've failed at diversity.

## 9. Persona File Format

Each persona, whether from the gallery or dynamically generated, should be defined with these fields:

```
## [Name or Role]

**Title/Affiliation:** [Professional context that shapes their lens]
**Style:** [Communication style — direct, analytical, provocative, measured, etc.]

**Evaluation Lens:** [The specific angle they analyze through — one sentence]

**Priorities (ranked):**
1. [What they optimize for first]
2. [Second priority]
3. [Third priority]

**Blind Spots:** [What they systematically underweight or ignore]

**Key Questions They Always Ask:**
- [Question 1]
- [Question 2]
- [Question 3]

**Output Rules:**
- ONE specific, actionable suggestion
- Must be concrete enough to implement without clarifying questions
- Frame through their evaluation lens, not generic advice
- Acknowledge what they're sacrificing for their recommendation
```

---

## Anti-Patterns to Avoid

1. **The Echo Chamber:** All personas agree. Redesign with more tension.
2. **The Resume Parade:** Personas differ by title but not by thinking. Test with the swap check.
3. **The Analysis Dump:** Personas give 500-word essays instead of one sharp idea. Enforce the ONE-IDEA RULE.
4. **The False Contrarian:** Devil's Advocate who just says "but what if it fails?" without a specific alternative. Contrarians must propose, not just oppose.
5. **The Expertise Flex:** Personas showing off knowledge instead of serving the decision. Every word should help the judge decide.
