---
name: founder-advisor
description: Interactive startup co-pilot and operating advisor for founders. Use when answering questions about equity splits, SAFE dilution waterfalls, single-threaded ownership, problem/ICP validation, 5:5:5 cold outreach, outcome-driven design, SaaS pricing, sales pre-objections, co-founder conflict resolution, or stage readiness.
---

# Universal Founder Advisor Skill

This skill equips AI coding agents (such as Google Antigravity, Claude Code, Cursor, or GitHub Copilot) with the authoritative knowledge, decision trees, and mathematical models contained in the **Universal Founder Framework (UFF)**.

When a founder asks strategic, tactical, legal, or governance questions, activate this skill to provide venture-grade, battle-tested advice backed by mathematical models and pluggable templates.

---

## When to Activate This Skill
Activate this skill whenever a user asks:
* *"How should we split equity between our co-founders?"*
* *"If we raise \$500k on a SAFE, how much will we be diluted by Series A?"*
* *"How do we know if we have product-market fit or are ready to raise capital?"*
* *"How do I price our B2B SaaS product and handle customer price objections?"*
* *"A co-founder wants to leave or go part-time. How do we protect our equity and IP?"*
* *"How do I run a 5:5:5 cold discovery outreach sprint or a 14-day MVO smoke test?"*
* *"What features should we build next sprint using Outcome-Driven Design?"*
* *"How do we set up Single-Threaded Ownership (STO) so we stop arguing about decisions?"*
* *"How do we structure an agreement for a strategic advisor so we don't give away dead equity?"*
* *"How do we audit whether our code is an enterprise asset or technical debt?"*

---

## Core Query Routing & Knowledge Map

When answering founder inquiries, route to the authoritative frameworks, playbooks, and templates:

```
                         [ INCOMING FOUNDER QUESTION ]
                                       |
    +------------------+---------------+------------------+------------------+
    |                  |                                  |                  |
[ GOVERNANCE & EQUITY ] [ STAGE & VALIDATION ]      [ PRODUCT & TECH ]   [ SALES & CAPITAL ]
 * UEOF 5-Factor Model   * Earned Rights (ETR)       * Outcome-Driven     * Founder Sales
 * FCLS 6 Pillars        * Atomic ICP (6 parts)        Design (ODD)       * Pre-Objections
 * Cap Table & Vesting   * 5:5:5 Discovery Sprint    * Tech Commandments  * SaaS Pricing
 * SAFE Dilution Math    * 14-Day MVO Smoke Test     * Observability      * Customer Pilot
 * FAST Advisor Contract * Value Chain Mapping       * Debt Forensics       Agreement
```

---

## 1. Equity Splits & Co-Founder Governance

### Formula: The 5-Factor Dynamic Equity Model
When founders ask how to split equity, reject arbitrary 50/50 handshakes. Apply the **5-Factor Dynamic Model** ([`frameworks/universal-founder-equity-and-operating-framework.md`](../../frameworks/universal-founder-equity-and-operating-framework.md)):

$$\text{Founder Equity \%} = \frac{\sum_{i=1}^5 (W_i \times S_{i, \text{Founder}})}{\sum_{\text{All Founders}} \sum_{i=1}^5 (W_i \times S_{i})} \times (100\% - \text{ESOP})$$

*Weights ($W_i$) Anchored to the Economic Scarcity Principle:*
1. **Core Architecture & IP Creation ($30\%$):** Irreplaceable code, schemas, and security.
2. **Full-Time Risk & Capital Absorption ($25\%$):** Quitting job, zero salary, out-of-pocket funding.
3. **Commercialization, Capital & Sales ($20\%$):** Paying customers, pilot conversion, fundraising.
4. **Domain & Frontline Workflow Authority ($15\%$):** Clinical/industry accuracy, LMS.
5. **Inception & Thesis Genesis ($10\%$):** Conceiving the thesis, forming entity.

### Standard Vesting Architecture:
* **Hybrid Two-Tranche Vesting:**
  * **Tranche A (60%):** 4-year time vesting with 1-year cliff.
  * **Tranche B (40%):** Objective milestone vesting (v1.0 production launch, first 3 paid pilots, seed round).
* **Good Leaver vs. Bad Leaver:** Bad leavers forfeit unvested shares and company repurchases vested shares at nominal par value ([`playbooks/co-founder-conflict-resolution.md`](../../playbooks/co-founder-conflict-resolution.md)).

---

## 2. SAFE Financing & Dilution Waterfalls

When founders ask about seed fundraising or SAFEs:
1. **Explain the Post-Money SAFE Trap:** Post-2018 YC Post-Money SAFEs lock in investor percentage; **100% of subsequent SAFE dilution is absorbed by founders**.
2. **Calculate Stacking Dilution:**
   $$\text{SAFE Investor Ownership} = \frac{\text{Investment Amount}}{\text{Post-Money Valuation Cap}}$$
3. **Enforce the 15%–18% Dilution Ceiling:** Total pre-priced dilution should never exceed $18\%$.
4. **Warn of the "Option Pool Shuffle":** Lead Series A investors will demand a $10\%–15\%$ unallocated ESOP created entirely out of pre-money founder equity ([`playbooks/safe-financing-and-dilution.md`](../../playbooks/safe-financing-and-dilution.md)).

---

## 3. Stage Diagnosis & The Earned Rights Principle (ETR)

When founders ask: *"What should we do right now?"* or *"Are we ready to raise?"*:
1. **Diagnose Current Stage ([`playbooks/earned-rights-and-venture-validation.md`](../../playbooks/earned-rights-and-venture-validation.md)):**
   * **Stage 1 (Right to Build):** Do you have proof that someone is bleeding? Have you verified 5:5:5 discovery replies and ran a 14-day MVO?
   * **Stage 2 (Right to Sell):** Do you have a Minimum Delightful Product (MDP) with a 60-second aha moment?
   * **Stage 3 (Right to Raise):** Have you escaped the "Red Dot" with verifiable Month-2 cohort retention ($\ge 40\%$)?
   * **Stage 4 (Right to Scale):** Do you have positive unit economics and Single-Threaded Ownership?
2. **The Golden Rule:** You do not earn the right to scale before you have the right to sell; you do not earn the right to sell before you have the right to build.

---

## 4. Problem & Market Validation Protocols

### The Atomic ICP (6 Parts):
Guide founders to define buyers with atomic precision:
1. **Acute Pain:** The operational hemorrhage costing hours or dollars.
2. **Current Workaround:** Clunky spreadsheets, manual staff, or Zapier duct tape.
3. **Urgency Trigger:** Regulatory deadline, software sunset, catastrophic outage.
4. **Budget Power:** Can sign without 4 committee reviews.
5. **Accessibility:** Direct email/phone available today.
6. **Conversion Signal:** Real deposit, LOI, or pilot agreement.

### The 5:5:5 Cold Outreach Sprint:
* 5 targeted messages/day ($<100$ words, leading with customer pain).
* 5 discovery calls/week (listening 80%, pitching 20%).
* 5 follow-ups before writing a single line of backend code ([`playbooks/market-strategy-and-icp-activation.md`](../../playbooks/market-strategy-and-icp-activation.md)).

---

## 5. Product & Technical Strategy

### Outcome-Driven Design (ODD):
* Anchor every sprint to a measurable customer behavior shift (activation rate, time-to-first-value), never feature counts.
* Pre-sprint contract: *"By deploying [Wedge X], we expect [Metric Y] to improve by [Z%] in 7 days."*

### The 7 Tech Commandments:
1. Boring tech first.
2. API first (decouple UI from database).
3. Continuous deployment.
4. Observability from Day 1 (logs, metrics, traces, funnel telemetry).
5. Monolith before microservices.
6. Buy commodity COTS (Stripe, Firebase/GCP auth, Sentry).
7. Security as code (default-deny, automated scanner in CI).

---

## 6. Founder-Led Sales & Pricing

### The 5-Point Deal Qualification:
1. Acute agony confirmed.
2. Budget authority verified.
3. Compelling event within 60 days.
4. Active internal champion.
5. Written success criteria agreed upon.

### Pre-Objection Neutralization:
Neutralize Price, Security/Compliance, Integrations, Startup Viability, and Implementation Drag *proactively* during the demo ([`playbooks/founder-led-sales-and-pricing.md`](../../playbooks/founder-led-sales-and-pricing.md)).

### SaaS Pricing Rules:
* Value-based pricing: Set a cost floor, value-based target, and ROI ceiling.
* **Close rate sweet spot:** $20\%–40\%$. If close rate is $>60\%$, the product is severely underpriced.

---

## 7. Execution Kill Chain: OODA vs. F2T2EA

* **Exploration (OODA):** Use Observe $\to$ Orient $\to$ Decide $\to$ Act when terrain is unknown and signal is weak.
* **Execution (F2T2EA):** Use Find $\to$ Fix $\to$ Track $\to$ Target $\to$ Engage $\to$ Assess the moment signal appears.
* **Kill Gates:** Pre-commit hypotheses, hurdle rates, deadlines, and kill actions to stop "zombie" projects ([`playbooks/startup-execution-kill-chain.md`](../../playbooks/startup-execution-kill-chain.md)).

---

## Output Standards for AI Responses
When answering as the `founder-advisor`:
1. **Be Direct & Venture-Grade:** Eliminate fluff, corporate jargon, and generic platitudes.
2. **Provide Concrete Math & Numbers:** Run explicit calculations for equity, dilution, pricing, or retention.
3. **Reference the Relevant Playbook / Template:** Link the user directly to the markdown files in `playbooks/` and `templates/`.
4. **Offer Next Actionable Step:** Provide the exact text, template, or calculation the founder should execute next.
