---
name: equity-calculator
description: Calculate founder equity allocations, Frank Demmler's Founder's Pie, and Post-Money SAFE dilution waterfalls with Series A option pool shuffle. Use when modeling co-founder splits, cap table dilution, SAFE notes, or unallocated option pools.
---

# Equity & SAFE Dilution Calculator Skill

This skill equips AI coding agents with the computational tools and mathematical models to calculate objective, venture-grade founder equity splits and model cap table dilution across SAFEs and priced equity rounds.

It is powered by the zero-dependency CLI tool [`tools/equity_calculator.py`](../../tools/equity_calculator.py).

---

## When to Activate This Skill

Activate this skill whenever a founder, co-founder, or advisor asks:
* *"How should we split equity between our 2 or 3 co-founders?"*
* *"Can you calculate our equity based on the 5-Factor Dynamic Equity Model?"*
* *"How do we run Frank Demmler's Founder's Pie Calculator?"*
* *"If we raise \$500k on a \$5M post-money SAFE and \$1M on a \$10M SAFE, how much equity do we keep?"*
* *"What happens to our cap table when an institutional Series A VC demands a 15% unallocated option pool?"*
* *"Can you model the SAFE dilution waterfall for our upcoming seed round?"*

---

## Tool Execution

The underlying calculator is located at `tools/equity_calculator.py`. It requires only standard Python 3.8+ (no `pip install` required).

### Command-Line Usage

```bash
# 1. 5-Factor Dynamic Equity Model (Default Universal Founder Framework)
python tools/equity_calculator.py --mode dynamic \
  --founders "Alice:9,8,7,6,8" "Bob:5,10,8,9,6" \
  --esop 15

# 2. Frank Demmler's Founder's Pie Calculator (Carnegie Mellon Model)
python tools/equity_calculator.py --mode demmler \
  --founders "Alice:10,8,7,9,8" "Bob:6,9,9,10,7" \
  --esop 15

# 3. Post-Money SAFE Dilution Waterfall & Series A Option Pool Shuffle
python tools/equity_calculator.py --mode safe \
  --safes "500000:5000000" "1000000:10000000" \
  --esop 15 \
  --series-a "5000000:25000000"

# 4. Built-in Demonstration of All Three Models
python tools/equity_calculator.py --demo

# 5. Programmatic JSON Output for Agent Workflows
python tools/equity_calculator.py --mode dynamic --founders "Alice:9,8,7,6,8" "Bob:5,10,8,9,6" --json
```

---

## 1. The 5-Factor Dynamic Equity Allocation Model

### The Economic Scarcity Principle
Reject 50/50 static splits. Equity allocation reflects **irreplaceability** and **future value creation**:

$$\text{Founder Equity \%} = \frac{\sum_{i=1}^5 (W_i \times S_{i, \text{Founder}})}{\sum_{\text{All Founders}} \sum_{i=1}^5 (W_i \times S_{i})} \times (100\% - \text{ESOP})$$

### Factor Scoring Rubric (Scores 1–10)

| Factor | Weight ($W_i$) | Scarcity Rationale | Scoring Guidance (1–10) |
|---|:---:|---|---|
| **1. Core Architecture & IP Creation** | **30%** | **Irreplaceable.** Foundational schemas, core IP, distributed backend, security posture. | 10 = Authored production architecture; 5 = Contributed features; 1 = No code. |
| **2. Full-Time Commitment & Risk** | **25%** | **High Scarcity.** Quitting salary, personal capital risk, unhedged operational focus. | 10 = Full-time Day 0 without pay; 5 = Transitioning in 6 mo; 2 = Moonlighting. |
| **3. Commercialization & Sales** | **20%** | **High Scarcity.** Closing pilot agreements, commercial contracts, institutional capital. | 10 = Closed paying enterprise pilots; 5 = Building pipeline; 1 = No sales activity. |
| **4. Domain & Frontline Authority** | **15%** | **Augmentable.** Industry workflows, clinical accuracy, operational insights. | 10 = 10+ yrs deep domain veteran; 5 = Generalist with domain exposure. |
| **5. Inception & Genesis** | **10%** | **One-Time Catalyst.** Ideation, forming legal entity, initial pitch deck. | 10 = Originated core thesis; 5 = Joined at inception; 2 = Joined post-ideation. |

---

## 2. Frank Demmler's Founder's Pie Model (Carnegie Mellon)

For teams preferring the traditional university venture methodology:

| Factor | Weight | Description |
|---|:---:|---|
| **Idea & Business Genesis** | **10%** | Original concept, market opportunity identification. |
| **Business Plan & Strategy** | **10%** | Financial modeling, strategy deck, go-to-market plan. |
| **Domain Expertise** | **20%** | Industry credibility, specialized domain skills. |
| **Commitment & Risk** | **25%** | Opportunity cost, salary sacrifice, full-time commitment. |
| **Responsibilities & Execution** | **35%** | Delivering product, leading teams, driving revenue. |

---

## 3. Post-Money SAFE Waterfall & Series A Dilution

### The SAFE Dilution Rule of Thumb
In a YC Post-Money SAFE, each SAFE investor's ownership is fixed at:

$$\text{Investor Ownership \%} = \frac{\text{Investment Amount}}{\text{Post-Money Valuation Cap}} \times 100\%$$

All SAFE dilution falls **exclusively on the founders** before Series A.

### The Option Pool Shuffle (Series A)
Institutional VCs typically mandate a **10% to 15% unallocated option pool** created *prior* to the investment (`pre-money`). This forces 100% of option pool dilution onto existing founders and SAFE holders, rather than sharing it with the new Series A investor.

The `tools/equity_calculator.py --mode safe` calculates:
1. SAFE investor ownership tranches.
2. Founder equity remaining post-SAFE financing.
3. Impact of pre-Series A option pool carveout (The Option Pool Shuffle).
4. Fully diluted post-Series A cap table across Founders, SAFEs, ESOP, and Series A Lead.

---

## Operational Guide for AI Agents

When interacting with a founder:
1. **Interview First:** Ask for each founder's role, commitment status (full-time vs part-time), and technical vs commercial contribution.
2. **Collect Scores:** Have the co-founders rate each other on the 5 factors (1–10).
3. **Execute CLI:** Run `tools/equity_calculator.py` to generate the mathematical split.
4. **Present Objectively:** Present the numbers alongside the economic rationale (irreplaceability vs hireability).
5. **Enforce 4-Year Vesting:** Remind founders that all equity must vest over 4 years with a 1-year cliff, regardless of the mathematical split.
