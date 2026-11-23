# AI-Native Architecture Lab

> **Research prototype (2026-11-23)** — Can autonomous coding agents complete changes more accurately and cheaply when code is organized by business domain? The AI-agent hypothesis is **not yet measured**.

## Runnable implementations

Six independent Java 21 / Spring Boot applications expose the same in-memory orders HTTP contract, with shared JUnit acceptance tests:

| Backend organization | Gradle run command | Port |
|---|---|---:|
| Layered | `gradle :baseline:backend:bootRun` | 8081 |
| AI-Native Domain Co-location | `gradle :apps:api:bootRun` | 8080 |
| DDD-inspired Aggregate | `gradle :variants:ddd:bootRun` | 8082 |
| Hexagonal / Ports & Adapters | `gradle :variants:hexagonal:bootRun` | 8083 |
| Vertical Slice | `gradle :variants:vertical-slice:bootRun` | 8084 |
| Modular Monolith | `gradle :variants:modular-monolith:bootRun` | 8085 |

Three React/Vite frontends: `baseline/frontend` (Layered), `apps/web` (AI-Native) and `variants/fsd-web` (FSD). From each directory, run `npm install && npm run dev`.

**Prerequisites:** JDK 21, Gradle 8.14+ on PATH, Node.js 22+, npm, Python 3.10+. The Gradle wrapper is not bundled. Servers store all state in memory.

All backends support:
- `POST /api/orders` -> 201 with order
- `GET /api/orders` -> 200 with sorted orders
- `POST /api/orders/{id}/cancel` -> 200, idempotent cancel
- Invalid create -> 400; non-existent ID -> 404

Details: [Runnable implementations & commands](docs/IMPLEMENTATIONS.md), [architecture comparability](docs/ARCHITECTURE_COMPARISON.md).

## Test commands

```bash
gradle :baseline:backend:test :apps:api:test :variants:ddd:test :variants:hexagonal:test :variants:vertical-slice:test :variants:modular-monolith:test
python3 scripts/validate_architecture.py
python3 scripts/validate_boundaries.py
python3 -m unittest discover -s benchmarks/tests -v
(cd baseline/frontend && npm install && npm run build)
(cd apps/web && npm install && npm run build)
(cd variants/fsd-web && npm install && npm run build)
```

CI runs the shared HTTP contract suite for six backend implementations and builds all three React apps. See [CI workflows](.github/workflows/ci.yml).

## Experiment data — two distinctly different datasets

### 1. Byte-identical source files, seven synthetic path layouts

Seven **identical source files** are copied into directory organizations inspired by Layered, AI-Native, DDD, Hexagonal, Vertical Slice, Modular Monolith, and FSD. Python times complete recursive lexical scanning. These synthetic layouts are **not full runnable pattern implementations**.

- [Report](results/latest/RESULTS.md) · [raw observations](results/latest/raw.csv) · [summary JSON](results/latest/summary.json)
- [Scan time SVG](results/latest/discovery_time.svg) · [files opened SVG](results/latest/discovery_files.svg)

### 2. Actual runnable source code, seven compositions

Different Java backends are paired with React sources, plus FSD frontend with Layered backend. Files, LOC and bytes differ, so timings are descriptive **not causally attributable to architecture**.

- [Report](results/runnable/RESULTS.md) · [raw observations](results/runnable/raw.csv) · [summary JSON](results/runnable/summary.json)
- [Scan time SVG](results/runnable/scan_latency.svg) · [source LOC SVG](results/runnable/source_lines.svg)

Both datasets use four search terms × 100 repeats per architecture profile, with machine/time/source hashes logged.

Re-run locally:

```bash
python3 scripts/benchmark_discovery.py --repeats 100 --output results/local
python3 scripts/benchmark_runnable.py --repeats 100 --output results/local-runnable
```

**These are not AI coding-agent measurements.** No AI model tokens, agent task completion rate, tool-call count, agent navigation time, or regression metric has been collected yet. See [agent experiment protocol](docs/EXPERIMENT.md) and [roadmap](docs/BENCHMARK_ROADMAP.md).

## Publication assets

- [Research blog draft: initial path-layout study](docs/BLOG_DRAFT.md)
- [Research blog draft: runnable implementations](docs/BLOG_02_RUNNABLE_BENCHMARK.md)
- [Portfolio text (Korean/English)](docs/PORTFOLIO_SNIPPET.md)
- [Architecture decision record](docs/ADR-0001-domain-colocation.md)
- [Agent instructions](AGENTS.md)

## Real AI source-discovery pilot (opt-in, not yet executed)

The repository includes an isolated, read-only Codex CLI trial runner. It records **real** model input/output tokens, elapsed seconds, command/tool calls, and precision/recall against pre-registered minimum code-change loci.

```bash
# Free dry run: prepares independent fixtures; does not call a model.
python3 scripts/agent_discovery_trial.py --profiles layered ai_native --runs 3

# Requires locally authenticated Codex CLI and can consume usage:
python3 scripts/agent_discovery_trial.py --execute --model YOUR_CODEX_MODEL --profiles layered ai_native ddd hexagonal vertical_slice modular_monolith fsd_frontend --runs 3
```

See [Codex experimental harness and safety notes](docs/AGENT_DISCOVERY_BENCHMARK.md). The read-only file-selection pilot is **distinct from autonomous code-edit success**. Local traces are gitignored; no AI metrics have been published yet.
