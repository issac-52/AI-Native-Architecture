#!/usr/bin/env python3
"""Measures lexical source scans on ACTUAL runnable architecture implementations.
NOT AI-agent browsing/search/coding performance. Different code bytes across profiles!
"""
import argparse
import csv
import hashlib
import json
import platform
import random
import statistics
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from benchmark_discovery import draw_chart

ROOT = Path(__file__).resolve().parents[1]
PROFILES = {
    "layered": ["baseline/backend/src/main/java", "baseline/frontend/src"],
    "ai_native": [
        "domains/order/backend/src/main/java", "domains/order/frontend",
        "apps/api/src/main/java", "apps/web/src",
    ],
    "ddd": ["variants/ddd/src/main/java", "baseline/frontend/src"],
    "hexagonal": ["variants/hexagonal/src/main/java", "baseline/frontend/src"],
    "vertical_slice": ["variants/vertical-slice/src/main/java", "baseline/frontend/src"],
    "modular_monolith": ["variants/modular-monolith/src/main/java", "baseline/frontend/src"],
    "fsd_frontend": ["baseline/backend/src/main/java", "variants/fsd-web/src"],
}
SEARCH_TERMS = ["cancel", "quantity", "productName", "Order"]
EXTENSIONS = {".java", ".js", ".jsx", ".ts", ".tsx"}


def file_paths(profile):
    files = []
    for folder in PROFILES[profile]:
        directory = ROOT / folder
        if not directory.is_dir():
            raise FileNotFoundError(directory)
        files.extend(f for f in directory.rglob("*") if f.is_file() and f.suffix in EXTENSIONS)
    return sorted(set(files))


def fingerprints(files):
    digest = hashlib.sha256()
    for path in files:
        digest.update(path.relative_to(ROOT).as_posix().encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def scan(profile, query):
    # Include recursive traversal in the measured duration. This is a plain lexical scan,
    # not a semantic index lookup and not an AI tool invocation.
    started = time.perf_counter_ns()
    files = file_paths(profile)
    opened = 0
    total_bytes = 0
    matching_files = 0
    hits = 0
    for path in files:
        payload = path.read_bytes()
        opened += 1
        total_bytes += len(payload)
        occurrences = payload.lower().count(query.lower().encode())
        if occurrences:
            matching_files += 1
            hits += occurrences
    return {
        "elapsed_ns": time.perf_counter_ns() - started,
        "files_opened": opened, "bytes_read": total_bytes,
        "matching_files": matching_files, "occurrences": hits,
    }


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeats", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20261123)
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "runnable")
    args = parser.parse_args(argv)
    if args.repeats < 1:
        parser.error("repeats must be > 0")
    args.output.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat()
    platform_id = platform.platform()
    meta = {}
    for profile in PROFILES:
        files = file_paths(profile)
        if not files:
            raise RuntimeError("No source files for " + profile)
        lines = sum(len(p.read_text(encoding="utf-8").splitlines()) for p in files)
        meta[profile] = {
            "source_sha256": fingerprints(files),
            "source_files": len(files),
            "source_lines": lines,
            "source_bytes": sum(p.stat().st_size for p in files),
            "source_roots": PROFILES[profile],
        }
    jobs = [(p, q, n) for p in PROFILES for q in SEARCH_TERMS for n in range(args.repeats)]
    random.Random(args.seed).shuffle(jobs)
    raw = []
    for profile, query, repeat in jobs:
        raw.append({
            "measured_at_utc": timestamp,
            "platform": platform_id,
            "python_version": platform.python_version(),
            "seed": args.seed, "profile": profile, "query": query, "repeat": repeat,
            "source_sha256": meta[profile]["source_sha256"],
            **scan(profile, query)
        })
    write_csv(args.output / "raw.csv", raw)
    groups = defaultdict(list)
    for row in raw:
        groups[(row["profile"], row["query"])].append(row["elapsed_ns"])
    summaries = [
        {
            "profile": profile, "query": query, "n": len(timing),
            "median_elapsed_ms": round(statistics.median(timing) / 1e6, 6),
            "source_files": meta[profile]["source_files"],
            "source_lines": meta[profile]["source_lines"],
            "source_bytes": meta[profile]["source_bytes"],
        }
        for (profile, query), timing in sorted(groups.items())
    ]
    write_csv(args.output / "summary.csv", summaries)
    aggregated = []
    for profile in sorted(PROFILES):
        subset = [s["median_elapsed_ms"] for s in summaries if s["profile"] == profile]
        aggregated.append({
            "profile": profile,
            "median_of_query_medians_ms": round(statistics.median(subset), 6),
            **meta[profile],
        })
    result = {
        "type": "real_runnable_code_lexical_scan_NOT_AI",
        "measured_at_utc": timestamp, "platform": platform_id,
        "python": platform.python_version(), "seed": args.seed, "repeats": args.repeats,
        "queries": SEARCH_TERMS, "profiles": aggregated,
        "warnings": [
            "Profiles contain DIFFERENT source code, sizes and abstraction levels.",
            "This is a full recursive lexical scan, NOT an AI model navigation measurement.",
            "No token use, task completion, code quality, or architecture superiority is measured."
        ]
    }
    (args.output / "summary.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    labels = [x["profile"] for x in aggregated]
    draw_chart(args.output / "scan_latency.svg", "Runnable source: full lexical scan",
               labels, [x["median_of_query_medians_ms"] for x in aggregated], "ms",
               "Different source sizes. Not an AI-agent speed comparison.")
    draw_chart(args.output / "source_lines.svg", "Runnable source: lines of code",
               labels, [x["source_lines"] for x in aggregated], "LOC",
               "Backend + paired React source. LOC is descriptive, not a quality score.")
    report = [
        "# Measured runnable-source comparison", "",
        "> **NOT a comparison of AI reasoning or AI coding productivity.** Actual code",
        "> from runnable architecture examples, searched by a Python lexical scanner.", "",
        f"- UTC: {timestamp}", f"- Platform: {platform_id}",
        f"- Repetitions: {args.repeats} per profile/query", f"- Seed: {args.seed}", "",
        "| Profile | Source files | Source LOC | Source bytes | Scan median (ms) |",
        "|---|---:|---:|---:|---:|",
    ]
    for x in aggregated:
        report.append(
            f'| {x["profile"]} | {x["source_files"]} | {x["source_lines"]} | '
            f'{x["source_bytes"]} | {x["median_of_query_medians_ms"]:.6f} |'
        )
    report += [
        "", "![Lexical full-scan time](scan_latency.svg)", "",
        "![Total source lines](source_lines.svg)", "",
        "## Interpretation",
        "- Each profile scans its full paired backend and frontend sources. These source files **differ**.",
        "- Extra abstractions naturally increase LOC/paths; no performance ranking is justified.",
        "- Shared HTTP contract tests measure functional parity, not coding-agent success.",
        "- A real AI benchmark requires the same agent, task, token budget, fresh checkouts and independent acceptance tests.",
        "", "Evidence: [raw.csv](raw.csv), [summary.csv](summary.csv), [summary.json](summary.json).",
        "", "Each profile's source roots and a SHA-256 fingerprint are recorded in summary.json.",
    ]
    (args.output / "RESULTS.md").write_text("\n".join(report) + "\n", encoding="utf-8")
    print(json.dumps({"profiles": len(aggregated), "raw_trials": len(raw), "output": str(args.output)}))
    return result


if __name__ == "__main__":
    main()
