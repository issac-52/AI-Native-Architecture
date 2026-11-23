#!/usr/bin/env python3
"""Run honest, read-only Codex discovery trials in isolated git repositories.

Unlike benchmark_discovery.py or benchmark_runnable.py this tool can run a real
LLM coding agent. It is deliberately NOT run in public CI: requires user's
local Codex authentication and may consume paid model usage. Dry run is free.

Primary research outcome: recall of two pre-registered code-change loci.
Secondary: precision, time, tokens, unique CLI tool calls. Does NOT measure
correctness of code edits, since the tasks are explicitly read-only.
"""
import argparse
import csv
import hashlib
import json
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

from benchmark_runnable import PROFILES, ROOT, file_paths, fingerprints
from benchmark_discovery import draw_chart

# Minimum source-change locations for TASK_T01. These are expert-proposed
# verification targets, not independently validated correctness proofs.
GOLD = {
    "layered": [
        "baseline/backend/src/main/java/lab/baseline/service/OrderService.java",
        "baseline/frontend/src/OrderApp.jsx",
    ],
    "ai_native": [
        "domains/order/backend/src/main/java/lab/ainative/order/OrderStore.java",
        "domains/order/frontend/OrderApp.jsx",
    ],
    "ddd": [
        "variants/ddd/src/main/java/lab/ddd/order/application/OrderApplicationService.java",
        "baseline/frontend/src/OrderApp.jsx",
    ],
    "hexagonal": [
        "variants/hexagonal/src/main/java/lab/hexagonal/application/service/OrderService.java",
        "baseline/frontend/src/OrderApp.jsx",
    ],
    "vertical_slice": [
        "variants/vertical-slice/src/main/java/lab/vertical/order/create/CreateOrder.java",
        "baseline/frontend/src/OrderApp.jsx",
    ],
    "modular_monolith": [
        "variants/modular-monolith/src/main/java/lab/modular/order/internal/OrderModule.java",
        "baseline/frontend/src/OrderApp.jsx",
    ],
    "fsd_frontend": [
        "baseline/backend/src/main/java/lab/baseline/service/OrderService.java",
        "variants/fsd-web/src/features/create-order/ui/CreateOrderForm.jsx",
    ],
}
PROMPT = (
    "This is a READ-ONLY code discovery task, NOT a request to edit files. "
    "We want to modify a web order management system so that quantities above "
    "100 return HTTP 400, and the frontend displays an actionable error. "
    "Identify the MINIMUM existing source files that require code changes, "
    "using repository-root-relative paths. Do not include tests, generated "
    "files, or documentation. Return only the required JSON object."
)
SCHEMA = {
    "type": "object",
    "properties": {
        "files": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["files"],
    "additionalProperties": False,
}
COMMON_AGENT_RULES = (
    "# Agent experiment\n\n"
    "Read-only discovery: do not edit files. Explore only this repository. "
    "Return repository-relative source file paths; no tests or documentation.\n"
)


def normalize_paths(files):
    if not isinstance(files, list) or any(not isinstance(x, str) for x in files):
        raise ValueError("files must be an array of strings")
    normalized = set()
    for value in files:
        path = value.strip().replace("\\", "/")
        while path.startswith("./"):
            path = path[2:]
        if not path or path.startswith("/") or ".." in Path(path).parts:
            raise ValueError("invalid relative path: " + value)
        normalized.add(path)
    return normalized


def score(found, expected):
    found, expected = set(found), set(expected)
    correct = len(found & expected)
    precision = correct / len(found) if found else 0.0
    recall = correct / len(expected) if expected else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "correct_loci": correct, "expected_loci": len(expected),
        "precision": round(precision, 6), "recall": round(recall, 6),
        "f1": round(f1, 6), "all_loci_found": int(expected <= found),
        "extra_paths": len(found - expected),
    }


def parse_codex_events(log_file):
    usage = {"input_tokens": 0, "cached_input_tokens": 0, "output_tokens": 0}
    completed = False
    started_tools = set()
    events = 0
    with Path(log_file).open(encoding="utf-8") as stream:
        for line in stream:
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            events += 1
            event_type = event.get("type", "")
            if event_type == "turn.completed":
                completed = True
                for key in usage:
                    usage[key] += int(event.get("usage", {}).get(key, 0) or 0)
            if event_type.startswith("item."):
                item = event.get("item", {})
                if item.get("type") in ("command_execution", "mcp_tool_call", "web_search"):
                    if item.get("id"):
                        started_tools.add(item["id"])
    return {**usage, "tool_calls": len(started_tools),
            "turn_completed": completed, "events": events}


def build_fixture(profile, destination, context="code-only"):
    destination = Path(destination)
    for filename in file_paths(profile):
        target = destination / filename.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(filename, target)
    (destination / "AGENTS.md").write_text(COMMON_AGENT_RULES, encoding="utf-8")
    if context == "native-docs" and profile == "ai_native":
        for folder in (
            "domains/order/specification", "domains/order/contract",
        ):
            source = ROOT / folder
            shutil.copytree(source, destination / folder, dirs_exist_ok=True)
        shutil.copy2(ROOT / "domains/order/AGENTS.md",
                     destination / "domains/order/AGENTS.md")
    subprocess.run(["git", "init", "-q"], cwd=destination, check=True)
    return destination


def file_state(directory):
    return {p.relative_to(directory).as_posix() for p in Path(directory).rglob("*")
            if p.is_file() and ".git" not in p.parts}


def run_trial(profile, trial, args, output, schema_file, git_sha):
    started_at = datetime.now(timezone.utc).isoformat()
    identifier = f"{profile}-T01-{trial:02d}"
    raw_log = output / (identifier + ".jsonl")
    final_message = output / (identifier + "-final.json")
    stderr_log = output / (identifier + ".stderr.txt")
    with tempfile.TemporaryDirectory(prefix="architecture-ai-scan-") as directory:
        fixture = build_fixture(profile, directory, args.context)
        before = file_state(fixture)
        command = [
            args.codex_bin, "exec", "--ephemeral",
            "--json", "--sandbox", "read-only",
            "--model", args.model, "--output-schema", str(schema_file),
            "--output-last-message", str(final_message), PROMPT,
        ]
        start = time.perf_counter()
        with raw_log.open("w", encoding="utf-8") as standard_out, \
                stderr_log.open("w", encoding="utf-8") as standard_err:
            try:
                proc = subprocess.run(command, cwd=fixture, stdout=standard_out,
                                      stderr=standard_err, timeout=args.timeout,
                                      check=False)
                exit_code = proc.returncode
            except subprocess.TimeoutExpired:
                exit_code = 124
        wall = round(time.perf_counter() - start, 3)
        unexpected_writes = len(file_state(fixture) - before)
    stats = parse_codex_events(raw_log)
    prediction, parsed = set(), False
    if final_message.exists():
        try:
            data = json.loads(final_message.read_text(encoding="utf-8"))
            prediction = normalize_paths(data["files"])
            parsed = True
        except (json.JSONDecodeError, KeyError, ValueError, TypeError):
            pass
    scored = (exit_code == 0 and stats["turn_completed"] and parsed
              and unexpected_writes == 0)
    gold = GOLD[profile]
    result = score(prediction, gold) if scored else {}
    return {
        "trial_id": identifier, "timestamp_utc": started_at,
        "base_sha": git_sha, "profile": profile, "task_id": "T01-discovery",
        "context": args.context, "model": args.model,
        "cli_version": args.cli_version, "source_sha256": fingerprints(file_paths(profile)),
        "prompt_sha256": hashlib.sha256(PROMPT.encode("utf-8")).hexdigest(),
        "exit_code": exit_code, "timed_out": int(exit_code == 124),
        "parsed": int(parsed), "valid_trial": int(scored),
        "wall_seconds": wall,
        "input_tokens": stats["input_tokens"],
        "cached_input_tokens": stats["cached_input_tokens"],
        "output_tokens": stats["output_tokens"],
        "tool_calls": stats["tool_calls"],
        "unexpected_writes": unexpected_writes,
        "correct_loci": result.get("correct_loci", ""),
        "expected_loci": len(gold),
        "precision": result.get("precision", ""),
        "recall": result.get("recall", ""),
        "f1": result.get("f1", ""),
        "all_loci_found": result.get("all_loci_found", ""),
        "extra_paths": result.get("extra_paths", ""),
        "predicted_files": json.dumps(sorted(prediction), ensure_ascii=False),
        "expected_files": json.dumps(gold, ensure_ascii=False),
        "raw_trace": raw_log.name, "final_response": final_message.name,
        "stderr_log": stderr_log.name,
    }


def write_report(output, rows):
    with (output / "trials.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    from statistics import median
    profiles = sorted({row["profile"] for row in rows})
    summaries = []
    for profile in profiles:
        valid = [r for r in rows if r["profile"] == profile and r["valid_trial"]]
        summaries.append({
            "profile": profile,
            "runs": sum(r["profile"] == profile for r in rows),
            "valid_runs": len(valid),
            "median_recall": round(median(r["recall"] for r in valid), 4) if valid else None,
            "median_wall_seconds": round(median(r["wall_seconds"] for r in valid), 3) if valid else None,
            "median_input_tokens": int(median(r["input_tokens"] for r in valid)) if valid else None,
        })
    (output / "summary.json").write_text(
        json.dumps({"experiment_type": "REAL_CODEX_READ_ONLY_DISCOVERY",
                    "not_implementation_success": True,
                    "profiles": summaries}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    valid_summaries = [r for r in summaries if r["valid_runs"]]
    if valid_summaries:
        labels = [s["profile"] for s in valid_summaries]
        draw_chart(output / "agent_recall.svg", "Codex: minimum file discovery recall",
                   labels, [100 * s["median_recall"] for s in valid_summaries], "%",
                   "Measured Codex read-only trials. Higher is better. Small sample sizes.")
        draw_chart(output / "agent_time.svg", "Codex: wall clock by layout",
                   labels, [s["median_wall_seconds"] for s in valid_summaries], "s",
                   "Measured end-to-end agent runtime; includes tool and model latency.")
    lines = [
        "# Actual Codex read-only discovery trials",
        "", "This file is generated ONLY after an authenticated local Codex run.",
        "The task is file selection, NOT autonomous implementation.",
        "", "| Profile | Valid / Runs | Median recall | Median wall time (s) | Median input tokens |",
        "|---|---:|---:|---:|---:|",
    ]
    for s in summaries:
        lines.append(
            f'| {s["profile"]} | {s["valid_runs"]}/{s["runs"]} | '
            f'{s["median_recall"] if s["median_recall"] is not None else "N/A"} | '
            f'{s["median_wall_seconds"] if s["median_wall_seconds"] is not None else "N/A"} | '
            f'{s["median_input_tokens"] if s["median_input_tokens"] is not None else "N/A"} |'
        )
    lines += [
        "", "Invalid or unparsed runs are counted but **not scored as passing**.",
        "Gold paths are expert-selected *minimum loci*, not a complete set of all viable changes.",
        "See trials.csv, per-run JSONL and stderr for auditability.",
    ]
    (output / "RESULTS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return summaries


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true",
                        help="Actually invoke authenticated Codex CLI (can incur charges).")
    parser.add_argument("--profiles", nargs="+", choices=sorted(PROFILES),
                        default=["layered", "ai_native"])
    parser.add_argument("--model", help="Pin an exact available Codex model; required for --execute")
    parser.add_argument("--runs", type=int, default=3)
    parser.add_argument("--seed", type=int, default=20261123)
    parser.add_argument("--context", choices=("code-only", "native-docs"), default="code-only")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "agent-local")
    args = parser.parse_args(argv)
    if args.runs < 1 or args.timeout < 1:
        parser.error("--runs and --timeout must be positive")
    if args.execute and not args.model:
        parser.error("--execute requires --model to pin the model")
    for profile in args.profiles:
        for gold in GOLD[profile]:
            if not (ROOT / gold).is_file():
                parser.error(f"Gold file missing for {profile}: {gold}")
    print(f"Profiles: {args.profiles}; runs/profile: {args.runs}; context: {args.context}")
    if not args.execute:
        with tempfile.TemporaryDirectory() as folder:
            for profile in args.profiles:
                path = build_fixture(profile, Path(folder) / profile, args.context)
                print(f"DRY RUN {profile}: {len(file_state(path))} isolated fixture files")
        print("No Codex invoked, no AI data produced. Use --execute --model MODEL.")
        return 0
    if not shutil.which(args.codex_bin):
        parser.error("Codex CLI not found on PATH; install and authenticate it locally")
    args.cli_version = subprocess.run([args.codex_bin, "--version"], capture_output=True,
                                     text=True, check=True).stdout.strip()
    sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout.strip()
    args.output.mkdir(parents=True, exist_ok=True)
    schema_file = args.output.resolve() / "response-schema.json"
    schema_file.write_text(json.dumps(SCHEMA, indent=2), encoding="utf-8")
    jobs = [(profile, i) for profile in args.profiles for i in range(1, args.runs + 1)]
    random.Random(args.seed).shuffle(jobs)
    rows = []
    for profile, trial in jobs:
        result = run_trial(profile, trial, args, args.output.resolve(), schema_file, sha)
        print(result["trial_id"], "valid=" + str(result["valid_trial"]),
              "recall=" + str(result["recall"]), "wall_s=" + str(result["wall_seconds"]))
        rows.append(result)
    summary = write_report(args.output, rows)
    print("Recorded", len(rows), "real Codex runs to", args.output)
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
