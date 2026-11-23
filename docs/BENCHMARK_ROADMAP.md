# Architecture benchmarking roadmap (2026-11-23)

## Stage 0 — complete: controlled lexical path experiment
- Identical source content in seven synthetic path layouts.
- Four queries × 100 repetitions/profile; 2,800 raw observations.
- CSV/JSON/Markdown/SVG artifacts archived by GitHub Actions.

## Stage 1 — first implementations complete, deeper conformance pending
- Six runnable Spring Boot API profiles: Layered, AI-Native, DDD, Hexagonal, Vertical Slice, Modular Monolith.
- Three runnable React builds: conventional, AI-Native, Feature-Sliced Design.
- Shared JUnit HTTP contract suite across all six backends.
- Basic dependency boundary checks for DDD/Hexagonal/FSD/Modular.
- Actual runnable-code lexical scans, with separately archived CSV/JSON/SVG.
- **Not complete:** cross-domain contracts, deeper modular-boundary enforcement, realistic domain complexity, rich DDD value objects and event flows.

## Stage 2a — pilot harness built; real Codex measurements pending
- `scripts/agent_discovery_trial.py` builds isolated Git fixtures with only the assigned architecture.
- Uses Codex `exec --json --sandbox read-only` with a pinned model and identical prompt.
- Pre-registered T01 minimum source-file loci; reports precision/recall, wall time, tokens and tool calls.
- Tests validate scoring, event parsing and fixture isolation **without making model calls**.
- Actual authenticated Codex trial execution has not occurred in this project session. Local authentication is required, and model usage may incur charges.
- Data remains local in gitignored `results/agent-local/` until reviewed for publication.

## Stage 2b — not yet started: autonomous implementation benchmark
- Freeze versioned, independent evaluator-owned tests for each task in `experiments/tasks.md`.
- Compare identical task prompts, pinned model/reasoning/tool settings, budgets, fresh fixtures, randomized order and >=3 trials/profile.
- Measure accepted task completion, regressions, external file modifications, time, tokens and interventions.
- Separate layout effects from agent instructions (e.g. 2×2 experiment); do not use mere path-layout proxy timings as evidence.

## Stage 3 — cross-domain scale
- Implement order/payment/inventory domain interactions with idempotency and deliberately injected failure.
- Add 10×/100× realistic source-tree complexity after maintaining equivalent business functionality.
- Report uncertainty, repeated samples and limitations; do not infer general architecture superiority from one demonstration.

## Stage 4 — public portfolio and article
- Publish raw and processed evidence with Git SHA, source fingerprints and environment versions.
- Create blog/portfolio artifacts with precise evidence claims.
- Distinguish lexical search, read-only agent file discovery, and autonomous code-edit success as **three independent findings**.
