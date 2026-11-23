# Agent instructions — comparative architecture laboratory

This is a controlled experiment, not production software.

1. Read `README.md`, `docs/IMPLEMENTATIONS.md`, `docs/EXPERIMENT.md` and `docs/ARCHITECTURE_COMPARISON.md`.
2. Backends: `baseline/backend`, `apps/api` + `domains/order/backend`, and `variants/{ddd,hexagonal,vertical-slice,modular-monolith}`. Frontends: `baseline/frontend`, `apps/web` + `domains/order/frontend`, and `variants/fsd-web`.
3. Always preserve the shared HTTP order contract unless explicitly changing its version and updating *all* variants during fixture preparation.
4. During a trial, modify only the assigned variant. Do **not** edit `benchmarks/contract-tests`, evaluator-owned acceptance checks, result CSV/JSON, graph outputs or the other variants.
5. The AI-Native domain variant must read `domains/order/AGENTS.md`, its domain specifications and OpenAPI contract.
6. FSD imports must respect layer direction; hexagonal inner ports and domain must not depend on Spring or adapters; modular consumers must use OrderFacade.
7. Report exact commands executed and test outcomes. Never claim unexecuted checks passed; do not invent AI benchmark findings.
8. Live deployment and destructive operations require explicit human approval.
