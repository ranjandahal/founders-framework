#!/usr/bin/env python3
"""
Universal Founder Framework — Dynamic Equity & SAFE Dilution Calculator
Standalone, zero-dependency tool implementing:
1. The 5-Factor Dynamic Equity Allocation Model (Universal Founder Framework)
2. Frank Demmler's Founder's Pie Calculator (Carnegie Mellon University)
3. Post-Money SAFE Stacking Dilution Waterfall & Series A Option Pool Shuffle

Usage:
  python tools/equity_calculator.py --mode dynamic --founders "Alice:9,8,7,6,8" "Bob:5,10,8,9,6" --esop 15
  python tools/equity_calculator.py --mode safe --safes "500000:5000000" "1000000:10000000" --esop 15 --series-a "5000000:25000000"
  python tools/equity_calculator.py --demo
"""

import sys
import argparse
import json

# ==============================================================================
# 1. THE 5-FACTOR DYNAMIC EQUITY ALLOCATION MODEL
# ==============================================================================

WEIGHTS_5_FACTOR = {
    "Core Architecture & IP Creation (Irreplaceable)": 30,
    "Full-Time Commitment & Risk Absorption (High Scarcity)": 25,
    "Commercialization, Capital & Sales (High Scarcity)": 20,
    "Domain & Frontline Authority (Hireable/Augmentable)": 15,
    "Inception & Thesis Genesis (One-Time Catalyst)": 10,
}

def calculate_dynamic_equity(founder_scores: dict, esop_percent: float = 15.0):
    """
    founder_scores format:
    {
       "Founder Name": [score1, score2, score3, score4, score5]  # values 1 to 10
    }
    """
    factors = list(WEIGHTS_5_FACTOR.keys())
    weights = list(WEIGHTS_5_FACTOR.values())
    total_weight = sum(weights)

    founder_weighted_points = {}
    for name, scores in founder_scores.items():
        if len(scores) != 5:
            raise ValueError(f"Founder {name} must have exactly 5 scores (1-10), got {len(scores)}")
        pts = sum(s * w for s, w in zip(scores, weights))
        founder_weighted_points[name] = pts

    total_pool_points = sum(founder_weighted_points.values())
    if total_pool_points == 0:
        raise ValueError("Total weighted points across all founders cannot be 0.")

    allocable_founder_equity = 100.0 - esop_percent

    results = {}
    for name, pts in founder_weighted_points.items():
        fraction = pts / total_pool_points
        founder_equity = fraction * allocable_founder_equity
        results[name] = {
            "weighted_points": round(pts, 2),
            "percentage_of_founder_pool": round(fraction * 100.0, 2),
            "fully_diluted_equity": round(founder_equity, 2),
        }

    return {
        "esop_reserve": esop_percent,
        "allocable_founder_equity": allocable_founder_equity,
        "total_points": total_pool_points,
        "founders": results
    }

# ==============================================================================
# 2. FRANK DEMMLER'S FOUNDER'S PIE CALCULATOR (CARNEGIE MELLON)
# ==============================================================================

DEMMLER_WEIGHTS = {
    "Idea & Business Genesis": 10,
    "Business Plan & Strategy Preparation": 10,
    "Domain Expertise & Track Record": 20,
    "Commitment & Risk (Full-time vs Part-time)": 25,
    "Responsibilities & Leadership Execution": 35,
}

def calculate_demmler_pie(founder_scores: dict, esop_percent: float = 15.0):
    weights = list(DEMMLER_WEIGHTS.values())
    founder_weighted_points = {}
    for name, scores in founder_scores.items():
        if len(scores) != 5:
            raise ValueError(f"Founder {name} must have exactly 5 scores (1-10) for Demmler Model")
        pts = sum(s * w for s, w in zip(scores, weights))
        founder_weighted_points[name] = pts

    total_pool_points = sum(founder_weighted_points.values())
    allocable_equity = 100.0 - esop_percent

    results = {}
    for name, pts in founder_weighted_points.items():
        fraction = pts / total_pool_points
        results[name] = {
            "points": round(pts, 2),
            "share_of_founders": round(fraction * 100.0, 2),
            "fully_diluted": round(fraction * allocable_equity, 2)
        }
    return {
        "esop_reserve": esop_percent,
        "founders": results
    }

# ==============================================================================
# 3. POST-MONEY SAFE WATERFALL & OPTION POOL SHUFFLE
# ==============================================================================

def calculate_safe_waterfall(safes: list, esop_expansion: float = 15.0, series_a: tuple = None):
    """
    safes: list of (investment_amount, post_money_cap)
    series_a: (investment_amount, post_money_valuation)
    """
    safe_shares = []
    total_safe_ownership = 0.0

    for idx, (inv, cap) in enumerate(safes):
        ownership = (inv / cap) * 100.0
        total_safe_ownership += ownership
        safe_shares.append({
            "safe_round": idx + 1,
            "investment": inv,
            "cap": cap,
            "ownership_locked": round(ownership, 2)
        })

    founder_remaining_pre_esop = 100.0 - total_safe_ownership

    # Pre-Series A ESOP Expansion (Option Pool Shuffle)
    # The new option pool is carved out of the pre-money valuation (dilutes founders)
    founder_pre_a = founder_remaining_pre_esop - esop_expansion
    esop_pre_a = esop_expansion

    series_a_result = None
    if series_a:
        inv_a, post_a = series_a
        series_a_ownership = (inv_a / post_a) * 100.0
        dilution_factor = (100.0 - series_a_ownership) / 100.0

        series_a_result = {
            "series_a_investment": inv_a,
            "series_a_post_money": post_a,
            "series_a_investor_equity": round(series_a_ownership, 2),
            "post_series_a_founders": round(founder_pre_a * dilution_factor, 2),
            "post_series_a_safes": round(total_safe_ownership * dilution_factor, 2),
            "post_series_a_esop": round(esop_pre_a * dilution_factor, 2),
        }

    return {
        "safes": safe_shares,
        "total_safe_dilution": round(total_safe_ownership, 2),
        "founder_equity_post_safes": round(founder_remaining_pre_esop, 2),
        "pre_series_a_esop_expansion": esop_expansion,
        "founder_equity_pre_series_a": round(founder_pre_a, 2),
        "series_a_waterfall": series_a_result
    }

# ==============================================================================
# CLI & DEMO HARNESS
# ==============================================================================

def print_demo():
    print("==================================================================")
    print("UNIVERSAL FOUNDER FRAMEWORK -- DYNAMIC EQUITY & DILUTION DEMO")
    print("==================================================================\n")

    print("--- 1. THE 5-FACTOR DYNAMIC EQUITY MODEL ---")
    demo_founders = {
        "Founder A (CTO / Arch)": [10, 10, 5, 8, 10],   # Arch:10, Risk:10, Comm:5, Dom:8, Incept:10
        "Founder B (CEO / Commercial)": [4, 10, 10, 6, 8], # Arch:4, Risk:10, Comm:10, Dom:6, Incept:8
        "Founder C (COO / Domain)": [3, 7, 6, 10, 4]      # Arch:3, Risk:7, Comm:6, Dom:10, Incept:4
    }
    eq = calculate_dynamic_equity(demo_founders, esop_percent=15.0)
    for name, data in eq["founders"].items():
        print(f"  * {name}:")
        print(f"      Weighted Points: {data['weighted_points']} pts")
        print(f"      Share of Founder Pool: {data['percentage_of_founder_pool']}%")
        print(f"      Fully Diluted Common Equity (after 15% ESOP): {data['fully_diluted_equity']}%")
    print(f"  * ESOP Unallocated Reserve: {eq['esop_reserve']}%\n")

    print("--- 2. POST-MONEY SAFE DILUTION WATERFALL ---")
    demo_safes = [
        (500000, 5000000),   # $500k on $5M Cap -> 10%
        (750000, 7500000),   # $750k on $7.5M Cap -> 10%
    ]
    waterfall = calculate_safe_waterfall(demo_safes, esop_expansion=12.0, series_a=(5000000, 25000000))
    print(f"  * Total SAFE Dilution (2 SAFEs): {waterfall['total_safe_dilution']}%")
    print(f"  * Founder Equity Post-SAFEs: {waterfall['founder_equity_post_safes']}%")
    print(f"  * Pre-Series A ESOP Expansion: -{waterfall['pre_series_a_esop_expansion']}%")
    print(f"  * Founder Equity Pre-Series A: {waterfall['founder_equity_pre_series_a']}%")
    
    sa = waterfall["series_a_waterfall"]
    print(f"\n  [ Series A Closing: $5M on $25M Post-Money (20.0% Round) ]")
    print(f"    - Series A Lead Investor: {sa['series_a_investor_equity']}%")
    print(f"    - Original Founders (Combined): {sa['post_series_a_founders']}%")
    print(f"    - Converted SAFE Investors: {sa['post_series_a_safes']}%")
    print(f"    - ESOP Reserve Pool: {sa['post_series_a_esop']}%")
    print("==================================================================")

def main():
    parser = argparse.ArgumentParser(description="Universal Founder Framework -- Dynamic Equity & SAFE Calculator")
    parser.add_argument("--mode", choices=["dynamic", "demmler", "safe"], help="Calculation mode")
    parser.add_argument("--demo", action="store_true", help="Run comprehensive demo scenario")
    parser.add_argument("--founders", nargs="+", help="Founder scores in format Name:s1,s2,s3,s4,s5")
    parser.add_argument("--esop", type=float, default=15.0, help="Unallocated ESOP reserve percentage (default: 15.0)")
    parser.add_argument("--safes", nargs="+", help="SAFEs in format investment:cap, e.g. 500000:5000000")
    parser.add_argument("--series-a", help="Series A in format investment:post_money, e.g. 5000000:25000000")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")

    args = parser.parse_args()

    if args.demo or len(sys.argv) == 1:
        print_demo()
        return

    if args.mode in ["dynamic", "demmler"]:
        if not args.founders:
            print("Error: --founders required. Example: --founders \"Alice:10,10,6,8,10\" \"Bob:4,10,10,6,8\"", file=sys.stderr)
            sys.exit(1)

        founder_scores = {}
        for f in args.founders:
            parts = f.split(":")
            if len(parts) != 2:
                print(f"Invalid founder format: {f}. Expected Name:s1,s2,s3,s4,s5", file=sys.stderr)
                sys.exit(1)
            name = parts[0].strip()
            scores = [float(x.strip()) for x in parts[1].split(",")]
            founder_scores[name] = scores

        if args.mode == "dynamic":
            res = calculate_dynamic_equity(founder_scores, esop_percent=args.esop)
        else:
            res = calculate_demmler_pie(founder_scores, esop_percent=args.esop)

        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print("\n=== EQUITY ALLOCATION RESULT ===")
            for name, d in res["founders"].items():
                print(f"Founder: {name}")
                for k, v in d.items():
                    print(f"  {k}: {v}")
            print(f"ESOP Reserve: {res.get('esop_reserve')}%")

    elif args.mode == "safe":
        if not args.safes:
            print("Error: --safes required. Example: --safes \"500000:5000000\" \"1000000:10000000\"", file=sys.stderr)
            sys.exit(1)
        safe_list = []
        for s in args.safes:
            inv, cap = s.split(":")
            safe_list.append((float(inv), float(cap)))

        series_a_tuple = None
        if args.series_a:
            inv_a, post_a = args.series_a.split(":")
            series_a_tuple = (float(inv_a), float(post_a))

        res = calculate_safe_waterfall(safe_list, esop_expansion=args.esop, series_a=series_a_tuple)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print("\n=== SAFE WATERFALL DILUTION RESULT ===")
            print(f"Total SAFE Dilution: {res['total_safe_dilution']}%")
            print(f"Founder Equity Post-SAFEs: {res['founder_equity_post_safes']}%")
            print(f"Pre-Series A ESOP Expansion: {res['pre_series_a_esop_expansion']}%")
            print(f"Founder Equity Pre-Series A: {res['founder_equity_pre_series_a']}%")
            if res.get("series_a_waterfall"):
                print("\nPost-Series A Capitalization:")
                for k, v in res["series_a_waterfall"].items():
                    print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
