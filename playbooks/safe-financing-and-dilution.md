# SAFE Financing & Cap Table Dilution Playbook
*Post-Money SAFEs, The Option Pool Shuffle, and Waterfall Mechanics*

> **Core Axiom:** Raising capital on SAFEs feels frictionless because you don't issue stock today. But stacking Post-Money SAFEs without modeling the dilution waterfall will quietly transfer 30% to 50% of your company to early checks before your priced round even begins.

---

## 1. The Post-Money SAFE Reality: What Founders Don't Realize

In 2018, Y Combinator shifted from the original Pre-Money SAFE to the **Post-Money SAFE**. 

While this provided institutional investors with certainty regarding their ownership percentage, it introduced a severe structural asymmetry: **all dilution from subsequent Post-Money SAFEs is absorbed 100% by the founders**.

```
       [ PRE-MONEY SAFE DILUTION ]                   [ POST-MONEY SAFE DILUTION ]
 SAFE investors and founders dilute each other      SAFE investors lock in their percentage;
       as new convertible notes enter.              ALL subsequent SAFEs dilute the founders alone.
         (FOUNDER FRIENDLY)                               (INVESTOR FRIENDLY)
```

### 1.1 The Post-Money SAFE Ownership Formula

$$\text{Ownership \% Locked by Investor} = \frac{\text{Investment Amount}}{\text{Post-Money Valuation Cap}}$$

*Example:* An angel invests $\$500,000$ on a $\$5,000,000$ Post-Money Valuation Cap.
$$\text{Investor Ownership} = \frac{\$500,000}{\$5,000,000} = 10.0\%$$
That $10.0\%$ is **guaranteed** regardless of how many other SAFEs are issued prior to the priced round.

---

## 2. The Compounding SAFE Stacking Trap

Founders frequently raise opportunistic rolling checks across 12 months at different caps. Notice how founder equity erodes while SAFE investors remain protected:

```
+-----------------------------------------------------------------------------------+
|                           THE SAFE STACKING WATERFALL                             |
|                                                                                   |
|  * Round 1: $250k on $4M Cap   ---> Locks in 6.25% equity                         |
|  * Round 2: $500k on $6M Cap   ---> Locks in 8.33% equity                         |
|  * Round 3: $750k on $8M Cap   ---> Locks in 9.38% equity                         |
|  * Round 4: $1,000k on $10M Cap---> Locks in 10.00% equity                        |
|                                                                                   |
|  TOTAL SAFE DILUTION SOLD: 33.96% (Founders own only 66.04% BEFORE Series A!)     |
+-----------------------------------------------------------------------------------+
```

---

## 3. The "Option Pool Shuffle" at Series A

When an institutional venture capital firm leads a Series A priced round, they routinely demand:
> *"The company must establish an unallocated Employee Stock Option Plan (ESOP) of 10% to 15% created prior to our investment."*

```
 [ Founders: 66.04% ]   ===>   [ Founders Forced to Absorb 15% ESOP ]   ===>   [ Series A Lead Takes 20% ]
                                  (Pre-Money Dilution on Founders)
                                  Founders drop from 66.0% to 51.0%              Founders drop to 40.8%!
```

### 3.1 The Dilution Waterfall Table

| Capitalization Event | Cash Injected | Post-Money Valuation | Founder Ownership | SAFE Pool | Option Pool | Series A Lead |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Day 1 Incorporation** | $\$0$ | — | **$100.0\%$** | $0\%$ | $0\%$ | $0\%$ |
| **Pre-Seed SAFEs (\$1.5M)** | $\$1,500,000$ | Various Caps | **$72.0\%$** | $28.0\%$ | $0\%$ | $0\%$ |
| **Pre-Series A ESOP Expansion** | $\$0$ | — | **$59.0\%$** | $28.0\%$ | $13.0\%$ | $0\%$ |
| **Series A (\$5M for 20%)** | $\$5,000,000$ | $\$25,000,000$ | **$47.2\%$** | $22.4\%$ | $10.4\%$ | **$20.0\%$** |

*Lesson:* Raising $\$1.5\text{M}$ on loose SAFEs followed by a standard Series A drops original founders to **under 50% ownership** before Series B even begins.

---

## 4. Venture-Grade Rules for Early-Stage Capital Raising

### Rule 1: The 15% Pre-Priced Dilution Ceiling
Establish an uncompromising corporate rule: **Never sell more than 15% to 20% of your company on SAFEs prior to your first priced equity round.**
$$\sum \left(\frac{\text{SAFE Check Size}}{\text{Post-Money Valuation Cap}}\right) \le 18\%$$

### Rule 2: Beware the "Most Favored Nation" (MFN) Trap
If you issue an uncapped SAFE with an MFN clause to an early angel, that angel automatically inherits the lowest valuation cap or highest discount you offer to any subsequent investor. Never grant MFN clauses without a strict expiration sunset or minimum cap floor.

### Rule 3: Side Letters & Information Rights
Limit full information rights and board observer seats to major institutional investors who purchase at least **$\ge 10\%$** of the round. Granting detailed monthly information rights to $\$25\text{k}$ angel checks creates severe administrative and confidentiality friction.

### Rule 4: Model the Cap Table Before Signing
Never accept an incoming wire before inputting the SAFE parameters into a cap table spreadsheet. If an incoming check moves your aggregate pre-priced dilution past $20\%$, raise the valuation cap or decline the capital.
