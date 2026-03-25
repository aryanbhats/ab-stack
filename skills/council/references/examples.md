# Worked Examples

Real council sessions that demonstrate the pattern in action. These show what good looks like — the level of specificity in personas, the ONE-IDEA RULE in practice, and how judge synthesis works.

---

## Example 1: Asset Management RAG Pipeline Financial Report Design Council

**Preset:** content (with finance-domain personas)
**Judge mode:** Assistant-as-Judge
**Question:** "What gives this report its IT factor? What single design element would most elevate the Concentrated Equity Fund annual report?"

### Personas (5 named professionals)

1. **Marcus Chen** — VP, Goldman Sachs Investment Communications
   - Lens: Institutional credibility and regulatory defensibility
   - Priorities: Clarity, compliance, trust signals
   - Style: Conservative, precise

2. **Priya Sharma** — Head of Product Design, Bloomberg Terminal
   - Lens: Information hierarchy and user experience
   - Priorities: Scanability, data density, progressive disclosure
   - Style: Direct, UX-focused

3. **James Whitfield** — Managing Director, Capital Markets
   - Lens: Client-facing impact and competitive positioning
   - Priorities: Differentiation from competitor reports, client retention
   - Style: Commercial, results-oriented

4. **Sarah Kim** — Creative Director, Pentagram
   - Lens: Visual design craft and emotional response
   - Priorities: Typography, color, whitespace, visual rhythm
   - Style: Aesthetic, opinionated

5. **David Aronov** — Quantitative Researcher, Two Sigma
   - Lens: Data presentation and statistical communication
   - Priorities: Accuracy, context for numbers, avoiding misleading visuals
   - Style: Analytical, precise

### Each persona's ONE suggestion

- **Marcus:** Add a "Regulatory Context" sidebar that maps each claim to its source — builds institutional trust.
- **Priya:** Add implication highlight boxes below key data points — "This means: [plain-English takeaway]" — bridges the gap between data and decision.
- **James:** Add a verdict box at the top of each section with a clear BUY/HOLD/SELL-equivalent signal — clients want the bottom line first.
- **Sarah:** Add a 4px accent stripe in brand blue (#0055A4) to the left edge of each recommendation box — creates visual hierarchy and brand identity without adding information density.
- **David:** Add key metric callouts in the margin — the 3 numbers that matter most, with sparkline context — readers should get the story from a 5-second scan.

### Judge Synthesis

The judge ranked suggestions by **effort-to-impact ROI**:

**Top 3 (implement now):**
1. **Accent stripe** (Sarah) — Pure CSS, zero content changes, immediate visual lift. Highest ROI.
2. **Implication highlight boxes** (Priya) — Moderate content effort, massive comprehension gain. The "IT factor" is making complex data feel obvious.
3. **Key metric callouts** (David) — Small design change, big scanability win. Works for the 80% of readers who won't read the full report.

**Deferred (need prerequisites):**
4. **Verdict box** (James) — Requires a rating/conviction system that doesn't exist yet. Good idea, but needs the rating framework first.
5. **Regulatory context sidebar** (Marcus) — Requires a source-mapping backend. Valuable for compliance but doesn't move the "IT factor" needle.

### Key Lesson

**Concrete beats abstract.** Every suggestion was implementable — Sarah's was literally a CSS property. The ONE-IDEA RULE forced each persona to commit to their BEST insight instead of listing 10 observations. The judge could compare apples-to-apples because each idea had a clear implementation cost and expected impact.

---

## Example 2: the-ab-index Content Platform Architecture Council

**Preset:** business (cross-domain: content + architecture + growth)
**Judge mode:** User-as-Judge (configured), but assistant played judge (design flaw that led to the User-as-Judge mode)
**Question:** "What's the right architecture for a Flask-based content command center that handles newsletter, social, and long-form content with SEO optimization?"

### Personas (3 strategic roles)

1. **Growth Strategist**
   - Lens: Audience acquisition math and channel economics
   - Priorities: Volume, conversion rates, unit economics per subscriber

2. **Systems Architect**
   - Lens: Technical implementation, security, maintainability
   - Priorities: Clean abstractions, security posture, operational simplicity

3. **Content Strategist**
   - Lens: Voice consistency, content quality, brand integrity
   - Priorities: Voice preservation at scale, editorial standards, audience trust

### Deliberation Highlights

**Growth Strategist** did the math:
- 335K realistic annual reach (not the 1M stretch goal)
- Required: 3 newsletters/week + 2 social posts/day + 1 long-form/week
- Unit economics: $0.12/subscriber acquisition cost target
- Verdict: The architecture must support HIGH VOLUME output without quality degradation

**Systems Architect** found security issues:
- localStorage for API tokens = XSS vulnerability
- Client-side API calls to Canvas/newsletter services = credential exposure
- Missing rate limiting on content generation endpoints
- Verdict: Move all API interactions server-side, implement proper session management

**Content Strategist** produced a voice degradation model:
- Identified 6 prohibitions for AI-assisted content (never fabricate quotes, never claim false credentials, never use superlatives without data, etc.)
- Created a "voice fingerprint" spec: sentence length distribution, vocabulary constraints, rhetorical patterns
- Verdict: Build voice validation into the pipeline, not as an afterthought

### 4 Points of Genuine Tension

1. **Volume vs. Quality:** Growth needs 3 newsletters/week; Content says quality degrades past 2. Resolution: 2 premium + 1 "quick take" format.

2. **Server-side vs. Client-side rendering:** Growth wants client-side SPA for speed; Architect says server-side for security. Resolution: Server-rendered with HTMX for interactivity.

3. **AI content generation scope:** Growth wants AI drafts for everything; Content says AI drafts for social only, human-written for long-form. Resolution: AI assists everywhere but human approves long-form, AI owns social drafts.

4. **Launch timeline:** Growth wants MVP in 2 weeks; Architect says security review alone takes a week. Resolution: 3-week timeline, security review parallel to UI work.

### Output

The proceedings document was 777 lines — the most comprehensive council output to date. It included a unified architecture spec that resolved all four tensions.

### Key Lesson (and Design Evolution)

**The council was NOT interactive.** The user wanted User-as-Judge mode — to read all analyses, deliberate, and make the calls. But the assistant synthesized and decided without presenting the anonymized analyses for user judgment. The user's verdicts on the 4 tensions came AFTER the assistant had already chosen.

This failure directly led to the two-mode judge design:
- **Assistant-as-Judge:** For code, general, research — where the assistant has domain competence to judge
- **User-as-Judge:** For finance, content, business, planning — where the user's judgment, values, and risk tolerance must drive the decision

The rule is simple: if the decision depends on personal values, risk appetite, or domain expertise the user has that the assistant doesn't, the user judges.

---

## Patterns Across Both Examples

1. **The ONE-IDEA RULE is the single highest-impact design choice.** It transforms rambling analysis into comparable, actionable suggestions.

2. **Named professionals work for creative/strategic domains.** Marcus, Priya, Sarah — the professional identity shapes HOW they think, not just WHAT they say.

3. **Functional roles work for technical domains.** Growth Strategist, Systems Architect — the evaluation axis matters more than the name.

4. **Tension is the value.** Both councils produced their best insights at the points of disagreement, not agreement. Design for tension.

5. **Proceedings documents are the artifact.** The council's value compounds over time when decisions are recorded with their reasoning. Future councils can reference past proceedings.
