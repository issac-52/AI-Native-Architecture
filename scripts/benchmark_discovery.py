#!/usr/bin/env python3
"""Measured lexical source-layout benchmark. Not a benchmark of AI-agent cognition.

Creates byte-identical code fixtures in multiple folder topologies. Measures full
filesystem walk + source keyword scan. Generates reproducible CSV/JSON/SVG/MD.
Only Python stdlib is used.
"""
import argparse
import csv
import hashlib
import json
import platform
import random
import statistics
import sys
import tempfile
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "baseline" / "backend" / "src" / "main" / "java" / "lab" / "baseline"
FRONT = ROOT / "baseline" / "frontend" / "src"
# Canonical files are *identical bytes* for every layout. They are topology-only
# fixtures; the Java packages/imports are NOT rewritten and fixtures are not runnable.
SOURCE = {
    "controller": SRC / "controller" / "OrderController.java",
    "service": SRC / "service" / "OrderService.java",
    "repository": SRC / "repository" / "OrderRepository.java",
    "model": SRC / "model" / "Order.java",
    "bootstrap": SRC / "BaselineApplication.java",
    "ui": FRONT / "OrderApp.jsx",
    "entry": FRONT / "main.jsx",
}
PROFILES = {
    "layered": {
        "controller": "backend/controller/OrderController.java",
        "service": "backend/service/OrderService.java",
        "repository": "backend/repository/OrderRepository.java",
        "model": "backend/model/Order.java",
        "bootstrap": "backend/Bootstrap.java",
        "ui": "frontend/pages/OrderApp.jsx",
        "entry": "frontend/app/main.jsx",
    },
    "vertical_slice": {
        "controller": "backend/features/order/OrderController.java",
        "service": "backend/features/order/OrderService.java",
        "repository": "backend/features/order/OrderRepository.java",
        "model": "backend/features/order/Order.java",
        "bootstrap": "backend/app/Bootstrap.java",
        "ui": "frontend/features/order/OrderApp.jsx",
        "entry": "frontend/app/main.jsx",
    },
    "ddd_context": {
        "controller": "backend/contexts/order/interfaces/OrderController.java",
        "service": "backend/contexts/order/application/OrderService.java",
        "repository": "backend/contexts/order/infrastructure/OrderRepository.java",
        "model": "backend/contexts/order/domain/Order.java",
        "bootstrap": "backend/bootstrap/Bootstrap.java",
        "ui": "frontend/order/OrderApp.jsx",
        "entry": "frontend/app/main.jsx",
    },
    "hexagonal": {
        "controller": "backend/order/adapters/inbound/http/OrderController.java",
        "service": "backend/order/application/usecase/OrderService.java",
        "repository": "backend/order/adapters/outbound/memory/OrderRepository.java",
        "model": "backend/order/domain/model/Order.java",
        "bootstrap": "backend/bootstrap/Bootstrap.java",
        "ui": "frontend/order/OrderApp.jsx",
        "entry": "frontend/app/main.jsx",
    },
    "fsd_frontend": {
        "controller": "backend/controller/OrderController.java",
        "service": "backend/service/OrderService.java",
        "repository": "backend/repository/OrderRepository.java",
        "model": "backend/model/Order.java",
        "bootstrap": "backend/Bootstrap.java",
        "ui": "frontend/pages/order/ui/OrderApp.jsx",
        "entry": "frontend/app/entry/main.jsx",
    },
    "modular_monolith": {
        "controller": "backend/modules/order/api/OrderController.java",
        "service": "backend/modules/order/application/OrderService.java",
        "repository": "backend/modules/order/infrastructure/OrderRepository.java",
        "model": "backend/modules/order/domain/Order.java",
        "bootstrap": "backend/app/Bootstrap.java",
        "ui": "frontend/modules/order/OrderApp.jsx",
        "entry": "frontend/app/main.jsx",
    },
    "ai_native": {
        "controller": "domains/order/backend/OrderController.java",
        "service": "domains/order/backend/OrderService.java",
        "repository": "domains/order/backend/OrderRepository.java",
        "model": "domains/order/backend/Order.java",
        "bootstrap": "apps/api/Bootstrap.java",
        "ui": "domains/order/frontend/OrderApp.jsx",
        "entry": "apps/web/main.jsx",
    },
}
QUERIES = ["cancel", "quantity", "productName", "Order"]


def source_hash():
    digest = hashlib.sha256()
    for key in sorted(SOURCE):
        if not SOURCE[key].is_file():
            raise FileNotFoundError(SOURCE[key])
        digest.update(key.encode("utf-8"))
        digest.update(SOURCE[key].read_bytes())
    return digest.hexdigest()


def prepare(root):
    for name, mappings in PROFILES.items():
        for key, relative in mappings.items():
            destination = root / name / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(SOURCE[key].read_bytes())


def scan(root, query):
    t0 = time.perf_counter_ns()
    # Exclude non-source files to avoid documentation dominating the measurement.
    files = sorted(p for p in root.rglob("*") if p.is_file() and p.suffix in (".java", ".jsx"))
    opened = 0
    total_bytes = 0
    matches = 0
    hits = 0
    for path in files:
        payload = path.read_bytes()
        opened += 1
        total_bytes += len(payload)
        count = payload.lower().count(query.encode("utf-8").lower())
        if count:
            matches += 1
            hits += count
    return {
        "elapsed_ns": time.perf_counter_ns() - t0,
        "files_opened": opened, "bytes_read": total_bytes,
        "matching_files": matches, "occurrences": hits,
    }


def rows_to_csv(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        out = csv.DictWriter(stream, fieldnames=fields)
        out.writeheader()
        out.writerows(rows)


def draw_chart(path, title, labels, vals, unit, note):
    w, h = 1030, 480
    left, right, top, bottom = 240, 100, 84, 70
    usable = w - left - right
    vmax = max(vals) if vals else 1
    if vmax == 0:
        vmax = 1
    row_h = (h - top - bottom) / max(1, len(labels))
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img">' % (w, h),
        '<rect width="100%" height="100%" fill="#0b1220"/>',
        '<text x="30" y="42" fill="#f8fafc" font-family="Arial,sans-serif" font-size="22" font-weight="bold">%s</text>' % escape(title),
        '<text x="30" y="63" fill="#94a3b8" font-family="Arial,sans-serif" font-size="12">%s</text>' % escape(note)
    ]
    for i, (label, val) in enumerate(zip(labels, vals)):
        y = top + i * row_h
        length = usable * val / vmax
        parts += [
            '<text x="24" y="%.1f" fill="#cbd5e1" font-family="Arial,sans-serif" font-size="15">%s</text>' % (y + 23, escape(label)),
            '<rect x="%d" y="%.1f" width="%.1f" height="25" rx="4" fill="#52b8ad"/>' % (left, y + 5, length),
            '<text x="%.1f" y="%.1f" fill="#f8fafc" font-family="Arial,sans-serif" font-size="14">%.3f %s</text>' % (left + length + 8, y + 23, val, unit),
        ]
    parts += ['</svg>']
    path.write_text("\n".join(parts), encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeats", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20261123)
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "local")
    args = parser.parse_args(argv)
    if args.repeats < 1:
        parser.error("--repeats must be positive")
    args.output.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat()
    fingerprint = source_hash()
    host = platform.platform()
    raw = []
    with tempfile.TemporaryDirectory(prefix="architecture-layouts-") as directory:
        fixtures = Path(directory)
        prepare(fixtures)
        trial_jobs = [(profile, query, i) for profile in PROFILES for query in QUERIES for i in range(args.repeats)]
        random.Random(args.seed).shuffle(trial_jobs)
        for profile, query, i in trial_jobs:
            measurement = scan(fixtures / profile, query)
            raw.append({
                "measured_at_utc": timestamp, "platform": host,
                "python": platform.python_version(), "source_sha256": fingerprint,
                "seed": args.seed, "profile": profile, "query": query, "repeat": i,
                **measurement,
            })

    fields = ["measured_at_utc", "platform", "python", "source_sha256", "seed",
              "profile", "query", "repeat", "elapsed_ns", "files_opened",
              "bytes_read", "matching_files", "occurrences"]
    rows_to_csv(args.output / "raw.csv", fields, raw)
    grouped = defaultdict(list)
    for item in raw:
        grouped[(item["profile"], item["query"])].append(item)
    summary = []
    for (profile, query), samples in sorted(grouped.items()):
        summary.append({
            "profile": profile, "query": query, "n": len(samples),
            "median_elapsed_ms": round(statistics.median(i["elapsed_ns"] for i in samples) / 1e6, 6),
            "files_opened": samples[0]["files_opened"],
            "bytes_read": samples[0]["bytes_read"],
            "matching_files": samples[0]["matching_files"],
            "occurrences": samples[0]["occurrences"],
        })
    rows_to_csv(args.output / "summary.csv",
                ["profile", "query", "n", "median_elapsed_ms", "files_opened",
                 "bytes_read", "matching_files", "occurrences"], summary)
    by_profile = defaultdict(list)
    for row in summary:
        by_profile[row["profile"]].append(row)
    aggregate = [
        {"profile": k, "median_of_query_medians_ms":
         round(statistics.median(r["median_elapsed_ms"] for r in values), 6),
         "files_opened": values[0]["files_opened"],
         "bytes_read": values[0]["bytes_read"],
         "query_count": len(values)}
        for k, values in sorted(by_profile.items())
    ]
    output = {
        "experiment_type": "lexical_layout_proxy_NOT_AI_agent",
        "measured_at_utc": timestamp, "source_sha256": fingerprint,
        "platform": host, "python": platform.python_version(), "seed": args.seed,
        "repeats_per_query": args.repeats, "queries": QUERIES, "profiles": aggregate,
        "warning": "Paths-only synthetic proxies; not full implementations. Differences are not AI-agent improvements.",
    }
    (args.output / "summary.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    labels = [p["profile"] for p in aggregate]
    draw_chart(args.output / "discovery_time.svg", "Lexical scan median by layout",
               labels, [p["median_of_query_medians_ms"] for p in aggregate], "ms",
               "Measured on one machine; not AI search latency. Lower is faster.")
    draw_chart(args.output / "discovery_files.svg", "Files opened per scan",
               labels, [p["files_opened"] for p in aggregate], "files",
               "All profiles contain identical source files by design.")
    lines = [
        "# Measured path-layout microbenchmark",
        "", "> **NOT AI performance evidence.** Identical source bytes, different paths; full lexical file scans.",
        "", "- UTC: " + timestamp,
        "- Platform: " + host,
        "- Source SHA-256: \`" + fingerprint + "\`",
        "- Repetitions per profile/query: " + str(args.repeats),
        "- Random seed: " + str(args.seed),
        "", "| Profile | Median of query medians (ms) | Files opened | Bytes read |",
        "|---|---:|---:|---:|",
    ]
    for p in aggregate:
        lines.append("| %s | %.6f | %d | %d |" % (
            p["profile"], p["median_of_query_medians_ms"], p["files_opened"], p["bytes_read"]))
    lines += [
        "", "![Discovery latency](discovery_time.svg)", "",
        "![Files opened](discovery_files.svg)", "",
        "## Interpretation",
        "This records real elapsed time on the named machine, not AI tokens, task success or semantic comprehension.",
        "Measurements may differ because of filesystem/cache noise and path lengths; do **not** infer architectural superiority.",
        "DDD, hexagonal and FSD are deeper design patterns that this paths-only fixture cannot fully implement.",
        "A proper agent experiment additionally requires pinned model, identical tasks, independent acceptance tests, repeated trials and tokens.",
        "", "Raw observations: [raw.csv](raw.csv) · Per-query summaries: [summary.csv](summary.csv).",
    ]
    (args.output / "RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Wrote", args.output)
    print(json.dumps(aggregate, indent=2))
    return output


if __name__ == "__main__":
    main()
