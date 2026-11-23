# Next steps for a defensible research benchmark

## Stage 0 — complete
- Two runnable reference applications: layer-oriented and domain-centered, same order API.
- Seven synthetic **path-layout proxy** fixtures using byte-identical source files.
- Automated lexical scans with recorded repeated observations.
- Repo-backed CSV, JSON and SVG reports.
- A CI mechanism that archives results and attempts to commit `results/latest/`.

## Stage 1 — upcoming
Build truly runnable implementations, starting with:
- Java Hexagonal: application port interfaces, inbound/outbound adapters, in-memory repository implementing an outbound port; dependency tests.
- Java DDD: bounded context, meaningful Order aggregate + domain rules, application service, persistence adapter.
- React FSD: distinct `app`, `pages`, `features`, `entities`, `shared` slices with public APIs and dependency lint rules.
- Vertical Slice: order create/list/cancel use-case slices with request handlers.
- Modular Monolith: modules with enforced boundaries and one process.
- AI-Native: manifest and domain-local FE/BE with validated dependency graph.

These should all pass the same end-to-end acceptance contract without being artificially forced into a single architectural category. A combined matrix (e.g. DDD + Hexagonal + FSD) is more meaningful than “winner takes all”.

## Stage 2 — real AI-Agent trials
- Freeze Git commit and model + tooling versions.
- Same task prompts (experiments/tasks.md), same budget and permissions.
- Fresh environment and randomized order; >=3 attempts per task/profile.
- Capture structured tool logs, input/output tokens, wall time and exit status.
- Hold acceptance tests separately, under evaluator control.
- Use human review only for specified risk gates, not to quietly repair outputs.
- Analyze success probability, regression, files changed outside expected scope, tokens and latency.
- Separately vary architecture, documentation and search/index tooling to control confounds.

## Stage 3 — scale and cross-domain complexity
- Order + payment + inventory with failures, idempotency and event contracts.
- 10x and 100x generated *behavioral* complexity only after equivalent implementations exist.
- Report uncertainty and avoid claiming generalizable speedups from one small project.

## Stage 4 — publish
- Export raw trials with environment and frozen version IDs.
- Generate comparative SVG/CSV and audit-ready Markdown.
- Blog and portfolio must link raw evidence, describe limitations and distinguish baseline measurements from agent experiments.
