# AI-Native Architecture Lab

An **experimental**, not yet validated, comparison between conventional layer-oriented and business-domain-centered FE/BE source organization for autonomous coding agents.

## Hypothesis
Keeping a feature's frontend, backend, contract, specifications and tests close together may improve an AI agent's task completion, navigation efficiency and change isolation. The outcome must be measured.

| Variant | Layout | Backend | Frontend |
|---|---|---|---|
| A: conventional | `baseline/backend` (controller/service/repository) and `baseline/frontend` | Spring Boot | React/Vite |
| B: AI-native | `domains/order/{backend,frontend,contract,specification,tests}` with `apps/{api,web}` entry points | Spring Boot | React/Vite |

Both implement the **same** in-memory order create/list/cancel API. No payment, inventory, authentication or durable storage.

## Prerequisites
JDK 21, Gradle 8.14+ installed on PATH, Node 22+, npm, Python 3.10+. (Gradle wrapper not bundled.)

## Run
**A:** `gradle :baseline:backend:bootRun` (port 8081), then `cd baseline/frontend && npm install && npm run dev` (http://localhost:5174).

**B:** `gradle :apps:api:bootRun` (port 8080), then `cd apps/web && npm install && npm run dev` (http://localhost:5173).

Each server stores orders in memory and resets on restart.

## Validate
```bash
python3 scripts/validate_architecture.py
gradle :baseline:backend:test :apps:api:test
(cd baseline/frontend && npm install && npm run build)
(cd apps/web && npm install && npm run build)
```

See [architecture](docs/ARCHITECTURE.md), [experiment protocol](docs/EXPERIMENT.md), [decision record](docs/ADR-0001-domain-colocation.md), [task catalog](experiments/tasks.md), [results CSV](experiments/results-template.csv) and [agent rules](AGENTS.md).

**Important:** this is a small single-domain proof of concept. Neither layout has measured AI performance results yet.

## Seven-layout measured discovery benchmark

The [benchmark suite](benchmarks/README.md) generates the **same seven files (same bytes) in seven different layout proxies**: layered, vertical slice, DDD context, hexagonal, FSD frontend, modular monolith and AI-native. It measures **deterministic lexical source scans**, not actual AI-Agent success or token efficiency. These synthetic layouts are **not runnable full implementations** of the named design methodologies.

Latest CI-generated measurements and presentation-ready vector charts:

- [Measured results report](results/latest/RESULTS.md)
- [Raw repeated observations (CSV)](results/latest/raw.csv)
- [Aggregated measurements (CSV)](results/latest/summary.csv)
- [Machine-readable results (JSON)](results/latest/summary.json)
- [Discovery time chart (SVG)](results/latest/discovery_time.svg)
- [Files opened chart (SVG)](results/latest/discovery_files.svg)
- [Benchmark workflow](.github/workflows/benchmark.yml)
- [Blog article draft](docs/BLOG_DRAFT.md) and [portfolio paragraph](docs/PORTFOLIO_SNIPPET.md)

Run locally:

```bash
python3 -m unittest discover -s benchmarks/tests -v
python3 scripts/benchmark_discovery.py --repeats 100 --output results/local
```

To claim that AI agents perform better, we still need a separately controlled **real agent task benchmark** with identical models/prompts and evaluator-owned acceptance tests. See [roadmap](docs/BENCHMARK_ROADMAP.md).
