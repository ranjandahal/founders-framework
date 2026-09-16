#!/usr/bin/env python3
"""
Universal Founder Codebase & Contribution Audit CLI
===================================================
A standalone, zero-external-dependency Python tool for founders, CTOs, and
venture investors to inspect Git telemetry, calculate surviving lines of code,
measure author churn, map subsystem ownership, and generate objective audit reports.

License: MIT
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


# Default file extensions to audit
DEFAULT_EXTENSIONS = {
    ".ts", ".tsx", ".js", ".jsx", ".go", ".py", ".rs", ".java",
    ".sql", ".html", ".css", ".vue", ".svelte", ".sh", ".ps1"
}

# Directories and files to strictly ignore
DEFAULT_IGNORED_DIRS = {
    "node_modules", ".git", "dist", "build", ".next", ".nuxt",
    ".vitepress/dist", ".vitepress/cache", "vendor", "coverage",
    "tmp", ".cache", "checkpoints"
}

DEFAULT_IGNORED_FILES = {
    "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "go.sum",
    "Cargo.lock", "poetry.lock", "composer.lock"
}


def run_git_command(repo_path, args):
    """Execute a git command in the target repo directory."""
    cmd = ["git", "-C", str(repo_path)] + args
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
            encoding="utf-8",
            errors="replace"
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return ""
    except Exception as e:
        return ""


def resolve_canonical_author(raw_author, raw_email, alias_map):
    """Map raw git author name or email to a canonical founder identifier."""
    if not alias_map:
        return raw_author or "Unknown"

    lookup_targets = [
        raw_author.lower() if raw_author else "",
        raw_email.lower() if raw_email else ""
    ]

    for canonical_name, aliases in alias_map.items():
        for alias in aliases:
            alias_lower = alias.lower()
            for target in lookup_targets:
                if target and (target == alias_lower or alias_lower in target):
                    return canonical_name

    return raw_author or "Unknown"


def get_tracked_files(repo_path, extensions, ignored_dirs, ignored_files):
    """Retrieve list of tracked files matching target extensions."""
    output = run_git_command(repo_path, ["ls-files"])
    if not output:
        return []

    valid_files = []
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue

        p = Path(line)
        parts = p.parts

        # Check ignored dirs
        if any(ignored in parts for ignored in ignored_dirs):
            continue

        # Check ignored file basenames
        if p.name in ignored_files:
            continue

        # Check extension
        if p.suffix.lower() in extensions:
            valid_files.append(line)

    return valid_files


def audit_blame(repo_path, tracked_files, alias_map):
    """Run git blame across tracked files to compute surviving lines per author."""
    author_lines = defaultdict(int)
    subsystem_lines = defaultdict(lambda: defaultdict(int))
    total_lines = 0

    for file_rel in tracked_files:
        full_path = Path(repo_path) / file_rel
        if not full_path.exists() or full_path.is_dir():
            continue

        # Classify subsystem
        subsystem = classify_subsystem(file_rel)

        # Run git blame --line-porcelain
        blame_out = run_git_command(repo_path, ["blame", "--line-porcelain", "--", file_rel])
        if not blame_out:
            continue

        curr_author = None
        curr_email = None

        for line in blame_out.splitlines():
            if line.startswith("author "):
                curr_author = line[7:].strip()
            elif line.startswith("author-mail "):
                curr_email = line[12:].strip().strip("<>")
            elif line.startswith("\t"):
                # Tab indicates the actual line content
                canonical = resolve_canonical_author(curr_author, curr_email, alias_map)
                author_lines[canonical] += 1
                subsystem_lines[subsystem][canonical] += 1
                total_lines += 1
                curr_author = None
                curr_email = None

    return author_lines, subsystem_lines, total_lines


def classify_subsystem(file_path):
    """Heuristically categorize file into a functional subsystem."""
    lower = file_path.lower()
    if any(s in lower for s in ["test", "spec", "__tests__", "e2e"]):
        return "Automated Tests"
    if any(s in lower for s in ["auth", "identity", "token", "jwt", "kms", "crypto", "security"]):
        return "Security & Identity"
    if any(s in lower for s in ["infra", "docker", "k8s", "terraform", ".github", "scripts"]):
        return "Infra & DevOps"
    if any(s in lower for s in ["schema", "model", "db", "firestore", "sql", "migration"]):
        return "Database & Schemas"
    if any(s in lower for s in ["api", "server", "service", "controller", "handler"]):
        return "Backend Services"
    if any(s in lower for s in ["ui", "component", "view", "page", "frontend", "client"]):
        return "Frontend & UI"
    if any(s in lower for s in ["doc", "docs", "specs", "guide"]):
        return "Documentation & Specs"
    return "Core Architecture"


def audit_commits(repo_path, alias_map):
    """Audit commit history, active days, and commit volume."""
    log_out = run_git_command(repo_path, ["log", "--format=%H|%aN|%aE|%ad", "--date=short"])
    if not log_out:
        return {}, {}

    author_commits = defaultdict(int)
    author_days = defaultdict(set)

    for line in log_out.splitlines():
        parts = line.strip().split("|")
        if len(parts) >= 4:
            c_hash, name, email, date_str = parts[0], parts[1], parts[2], parts[3]
            canonical = resolve_canonical_author(name, email, alias_map)
            author_commits[canonical] += 1
            author_days[canonical].add(date_str)

    author_active_days = {auth: len(days) for auth, days in author_days.items()}
    return author_commits, author_active_days


def audit_repository(repo_path, extensions, ignored_dirs, ignored_files, alias_map):
    """Perform complete forensic audit on a single repository."""
    repo_name = Path(repo_path).resolve().name
    tracked_files = get_tracked_files(repo_path, extensions, ignored_dirs, ignored_files)
    author_lines, subsystem_lines, total_lines = audit_blame(repo_path, tracked_files, alias_map)
    author_commits, author_days = audit_commits(repo_path, alias_map)

    return {
        "repo_name": repo_name,
        "repo_path": str(repo_path),
        "total_files": len(tracked_files),
        "total_surviving_lines": total_lines,
        "author_lines": dict(author_lines),
        "subsystem_lines": {k: dict(v) for k, v in subsystem_lines.items()},
        "author_commits": dict(author_commits),
        "author_days": dict(author_days)
    }


def aggregate_results(repo_results):
    """Aggregate multi-repo audit results into master metrics."""
    aggregated = {
        "total_repositories": len(repo_results),
        "total_surviving_lines": 0,
        "total_files": 0,
        "total_commits": 0,
        "authors": defaultdict(lambda: {
            "surviving_lines": 0,
            "line_percentage": 0.0,
            "total_commits": 0,
            "active_days": 0,
            "repos_contributed_to": []
        }),
        "subsystems": defaultdict(lambda: defaultdict(int))
    }

    all_days = defaultdict(set)

    for r in repo_results:
        aggregated["total_surviving_lines"] += r["total_surviving_lines"]
        aggregated["total_files"] += r["total_files"]

        for author, lines in r["author_lines"].items():
            aggregated["authors"][author]["surviving_lines"] += lines
            aggregated["authors"][author]["repos_contributed_to"].append(r["repo_name"])

        for author, commits in r["author_commits"].items():
            aggregated["authors"][author]["total_commits"] += commits
            aggregated["total_commits"] += commits

        for author, days in r["author_days"].items():
            aggregated["authors"][author]["active_days"] += days

        for sub, auth_dict in r["subsystem_lines"].items():
            for auth, lines in auth_dict.items():
                aggregated["subsystems"][sub][auth] += lines

    # Calculate percentages
    tot_lines = aggregated["total_surviving_lines"] or 1
    for author, data in aggregated["authors"].items():
        data["line_percentage"] = round((data["surviving_lines"] / tot_lines) * 100, 2)

    # Convert defaultdict to regular dict
    aggregated["authors"] = dict(aggregated["authors"])
    aggregated["subsystems"] = {k: dict(v) for k, v in aggregated["subsystems"].items()}

    return aggregated


def render_markdown_report(aggregated, repo_results):
    """Generate a clean Markdown report with GitHub flavored tables."""
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tot_lines = aggregated["total_surviving_lines"]
    tot_repos = aggregated["total_repositories"]

    md = []
    md.append("# Founder Contribution & Codebase Forensics Audit Report")
    md.append(f"\n> **Generated On:** {now_str}  ")
    md.append(f"> **Repositories Audited:** {tot_repos} | **Surviving Production Lines:** {tot_lines:,}\n")
    md.append("---\n")

    md.append("## 1. Executive Summary & Author Share")
    md.append("\n| Author / Founder | Surviving Lines | % of Living Code | Total Commits | Active Days | Repositories Active |")
    md.append("| :--- | :---: | :---: | :---: | :---: | :--- |")

    # Sort authors by surviving lines
    sorted_authors = sorted(
        aggregated["authors"].items(),
        key=lambda x: x[1]["surviving_lines"],
        reverse=True
    )

    for author, data in sorted_authors:
        pct = data["line_percentage"]
        lines = data["surviving_lines"]
        commits = data["total_commits"]
        days = data["active_days"]
        repos = ", ".join(data["repos_contributed_to"]) or "N/A"
        md.append(f"| **{author}** | {lines:,} | **{pct}%** | {commits:,} | {days} | {repos} |")

    md.append("\n---\n")
    md.append("## 2. Subsystem Single-Threaded Ownership (STO) Breakdown\n")
    md.append("| Functional Subsystem | Primary Owner | Dominant Share | Subsystem Line Count |")
    md.append("| :--- | :--- | :---: | :---: |")

    for sub, auth_dict in sorted(aggregated["subsystems"].items()):
        sub_total = sum(auth_dict.values())
        if sub_total == 0:
            continue
        top_auth, top_lines = max(auth_dict.items(), key=lambda x: x[1])
        top_pct = round((top_lines / sub_total) * 100, 1)
        md.append(f"| **{sub}** | {top_auth} | **{top_pct}%** ({top_lines:,} lines) | {sub_total:,} |")

    md.append("\n---\n")
    md.append("## 3. Per-Repository Breakdown\n")

    for r in repo_results:
        r_name = r["repo_name"]
        r_tot = r["total_surviving_lines"]
        r_files = r["total_files"]
        md.append(f"### Repository: `{r_name}` ({r_tot:,} surviving lines across {r_files} files)\n")
        md.append("| Author | Surviving Lines | Share | Commits |")
        md.append("| :--- | :---: | :---: | :---: |")
        
        sorted_repo_auths = sorted(r["author_lines"].items(), key=lambda x: x[1], reverse=True)
        for auth, l in sorted_repo_auths:
            pct = round((l / (r_tot or 1)) * 100, 1)
            commits = r["author_commits"].get(auth, 0)
            md.append(f"| {auth} | {l:,} | {pct}% | {commits} |")
        md.append("\n")

    md.append("---\n")
    md.append("## 4. Methodology & Data Integrity Notes")
    md.append("* **Surviving Lines vs. Raw Logs:** This audit runs `git blame` against the current `HEAD` commit. It discounts transient churn, copy-paste rewrites, and deleted experiments to measure living architectural assets.")
    md.append("* **Lockfile & Asset Exclusion:** Generated lockfiles (`package-lock.json`), build bundles (`dist/`, `build/`), and third-party vendor libraries are strictly filtered out to prevent artificial inflation.")
    md.append("* **Tool Reference:** Generated via [`tools/founder_audit.py`](./tools/founder_audit.py). Part of the open-source **Universal Founder Framework**.\n")

    return "\n".join(md)


def main():
    parser = argparse.ArgumentParser(
        description="Forensic Founder Codebase & Contribution Audit CLI"
    )
    parser.add_argument(
        "--repos",
        nargs="+",
        help="Path(s) to local git repositories to audit"
    )
    parser.add_argument(
        "--config",
        help="Path to JSON configuration file"
    )
    parser.add_argument(
        "--output",
        default="founder-audit-report.md",
        help="Output Markdown report path (default: founder-audit-report.md)"
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        default="founder-audit.json",
        help="Output JSON artifact path (default: founder-audit.json)"
    )

    # Ensure UTF-8 output encoding on Windows consoles
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    args = parser.parse_args()

    # Load configuration if provided
    config = {}
    if args.config and os.path.exists(args.config):
        with open(args.config, "r", encoding="utf-8") as f:
            config = json.load(f)

    # Resolve repos
    target_repos = args.repos or config.get("repositories", ["."])
    alias_map = config.get("alias_map", {})
    extensions = set(config.get("extensions", DEFAULT_EXTENSIONS))
    ignored_dirs = set(config.get("ignored_dirs", DEFAULT_IGNORED_DIRS))
    ignored_files = set(config.get("ignored_files", DEFAULT_IGNORED_FILES))

    print(f"[INFO] Starting Founder Contribution Audit across {len(target_repos)} repository(ies)...")

    repo_results = []
    for r in target_repos:
        repo_p = Path(r).resolve()
        if not repo_p.exists():
            print(f"[WARN] Skipping missing path: {repo_p}", file=sys.stderr)
            continue
        if not (repo_p / ".git").exists():
            print(f"[WARN] Skipping non-git directory: {repo_p}", file=sys.stderr)
            continue

        print(f"  [SCAN] Inspecting: {repo_p.name}...")
        res = audit_repository(repo_p, extensions, ignored_dirs, ignored_files, alias_map)
        repo_results.append(res)

    if not repo_results:
        print("[ERROR] No valid Git repositories found to audit.", file=sys.stderr)
        sys.exit(1)

    print("  [CALC] Aggregating multi-repo forensics...")
    aggregated = aggregate_results(repo_results)

    # Write JSON output
    print(f"  [SAVE] Writing JSON artifact to: {args.json_output}")
    with open(args.json_output, "w", encoding="utf-8") as f:
        json.dump({
            "meta": {
                "generated_at": datetime.datetime.now().isoformat(),
                "repositories_count": len(repo_results)
            },
            "aggregated": aggregated,
            "repositories": repo_results
        }, f, indent=2)

    # Write Markdown output
    print(f"  [SAVE] Writing Markdown report to: {args.output}")
    md_content = render_markdown_report(aggregated, repo_results)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"[SUCCESS] Founder Audit complete! Reports generated: {args.output}, {args.json_output}")


if __name__ == "__main__":
    main()
