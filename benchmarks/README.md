# Architecture benchmarks

## Two separate questions

1. **Topology/discovery microbenchmark (automated):** Given **identical source file bytes**, does a directory organization change the effort of deterministic lexical discovery? This is **not an AI-Agent performance measurement**.
2. **Autonomous agent task benchmark (manual/harness integration required):** Which variant helps the **same pinned AI model** implement tasks correctly, with fewer tokens, fewer regressions and less time? **No real AI comparisons have been conducted yet.**

## Experimental profiles

`scripts/benchmark_discovery.py` copies the exact same seven conventional implementation files into seven temporary layouts. These are **synthetic path-layout proxies**, not full runnable implementations of DDD, FSD, hexagonal, vertical slices or modular monoliths. They are *inspired by their organization patterns*. Canonical implementations in `baseline/` and `domains/` remain the runnable A/B application.

| Profile | Domain organization | What is represented | What is NOT represented |
|---|---|---|---|
| layered | controller/service/repository + separate FE | traditional layer paths | multiple bounded contexts |
| vertical_slice | feature order, BE and FE separated | feature grouping | full vertical slice request handlers |
| ddd_context | order bounded-context folders | context naming | true aggregates, ubiquitous language |
| hexagonal | inbound adapters, application ports, outbound adapters | path placement | dependency inversion, tested adapters |
| fsd_frontend | React pages/features/entities and BE layers | FSD-inspired FE file placement | true FSD public API, dependencies |
| modular_monolith | modular domain backend + independent FE | module naming | enforceable module boundaries |
| ai_native | one order folder for BE, FE, spec scope | cross-stack proximity | AI reasoning/performance, security policies |

FSD is **primarily a frontend methodology**, whereas DDD models domains and hexagonal architecture organizes dependency directions. These techniques **can be composed**; they are not mutually exclusive competitors.

## Run locally

```bash
python3 scripts/benchmark_discovery.py --repeats 100 --output results/local
python3 -m unittest discover -s benchmarks/tests -v
```

Output:
- `raw.csv`: per profile × query × repeat measurements with platform and source hash
- `summary.csv`: grouped descriptive medians (not significance claims)
- `summary.json`: structured summary
- `discovery_time.svg`: chart of measured median lexical scan time
- `discovery_files.svg`: files opened (usually identical by experimental design)
- `RESULTS.md`: generated blog-friendly report with cautions

CI uploads all outputs as an artifact and on a push to `main` attempts to persist `results/latest/` as a commit. GitHub repository permissions can block that commit; the downloadable workflow artifact is retained as a fallback.

## What is actually measured?

Each run recursively discovers `.java` and `.jsx` under the generated fixture, reads **every file** and counts case-insensitive occurrences of the query. The timer wraps recursive traversal and full-file search. Results include time, files opened, bytes read and matching files. File order is deterministic (sorted), and trial order is randomized with a fixed seed to reduce order bias.

**Expected result:** All layouts read the same files and bytes; measured time differences can be microsecond-scale noise from filesystem cache, file-name length and CI runner load. These results should never be presented as AI speedups.

## Agent benchmark protocol

Use `experiments/tasks.md` with a pinned agent/model and identical run budgets; do not use this lexical scanner as a proxy for token usage or task correctness. Run separate trials with fresh checkouts, evaluator-controlled acceptance tests and blind diffs. Store real agent trials in `experiments/results-template.csv`-compatible format. See [experimental methodology](../docs/EXPERIMENT.md).

## References

- [Official Feature-Sliced Design](https://feature-sliced.design/docs/get-started/overview)
- [AWS: Hexagonal and DDD](https://docs.aws.amazon.com/prescriptive-guidance/latest/hexagonal-architectures/overview.html)
- [Microsoft: Common web application architectures](https://learn.microsoft.com/en-us/dotnet/standard/modern-web-apps-azure-architecture/common-web-application-architectures)
