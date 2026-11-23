# Real AI Agent source discovery experiment — Codex CLI

> **Status: runner implemented, real Codex trials NOT YET EXECUTED.** No artificial/fabricated AI metrics are committed.

This is the missing bridge between deterministic Python grep timing and actual AI search/navigation performance.

The runner creates a **fresh isolated Git repository** containing only one profile's Java+React source code, randomizes trial order, and asks a pinned Codex model, in a **read-only sandbox**, to identify minimum code files for a quantity validation + UI error change. It does NOT ask the agent to implement the change.

Official non-interactive CLI reference: https://learn.chatgpt.com/docs/non-interactive-mode

## Cost-free preparation

From the repository root:

```bash
python3 -m unittest discover -s benchmarks/tests -v
python3 scripts/agent_discovery_trial.py --profiles layered ai_native --runs 3
```

The second command is a **dry run**: it only builds isolated fixtures and validates gold paths. It does not run AI or create benchmark results.

## Real trials (requires locally installed and authenticated Codex)

Choose a model actually available in your Codex account; pin its **exact identifier**:

```bash
python3 scripts/agent_discovery_trial.py --execute --model YOUR_CODEX_MODEL --profiles layered ai_native ddd hexagonal vertical_slice modular_monolith fsd_frontend --runs 3 --output results/agent-local
```

Each run can consume model usage. The script does not accept or write API keys, does not print credentials, does not call the CLI in GitHub Actions, and uses `--sandbox read-only --ephemeral`. It copies **only public study source files** to temporary isolated Git fixtures. Inspect logs before sharing; do not commit local traces blindly.

## What gets measured

- **Recall and precision** of two pre-registered, minimum relevant file loci for T01 (upper-bound validation + UI error message).
- **Wall-clock seconds** from CLI invocation through completion.
- **Input, cached-input and output tokens** from `turn.completed.usage` JSONL events.
- **Unique CLI tool calls** counted by `item.id`.
- Failure, timeout, unexpected writes, invalid output; failed parsing is **not silently counted as a success**.
- Model version, Codex CLI version, source fingerprint, base Git commit, prompt hash, UTC timestamp.

Files under `results/agent-local/`:
- `trials.csv`: one row per actual execution
- `summary.json`: aggregated empirical results
- `agent_recall.svg`, `agent_time.svg`: only when valid trials exist
- `RESULTS.md`: generated publishable report
- JSONL raw events and CLI stderr for independent review

## Caveats

1. **File selection is not code-change success.** Gold paths are proposed minimum loci, not the only correct implementation choices.
2. Token and time variation can reflect network latency, model updates, model reasoning effort, or nonuniform tool availability.
3. The default `--context code-only` excludes spec/AGENTS.md except a shared generic instruction to isolate structure effects. The optional `--context native-docs` adds AI-Native's domain docs, which intentionally changes the *context* variable and must be analyzed separately.
4. All runs use independent temporary Git repositories to prevent a model from seeing alternative architectures during one trial.
5. At least three trials per profile is a useful pilot, not enough to claim general superiority. Report error bars and replicate on different dates and tasks.
6. The runner does NOT include an automated coding-agent task benchmark with evaluator-controlled functional tests yet. That remains the next research stage.

## Privacy and publication

Codex authentication is local to your installed CLI; never commit `auth.json` or keys. Review raw agent logs and redact unexpected private content before manually publishing. The output directory is gitignored by default.
