# Agent instructions — architecture experiment

1. Read README.md, docs/ARCHITECTURE.md and docs/EXPERIMENT.md.
2. This is an **A/B experiment**. During a trial change only the assigned variant. Never modify evaluator-owned tests, metrics or the opposite variant.
3. For B read domains/order/AGENTS.md, specification/*.yaml and contract/openapi.yaml first.
4. Preserve API parity between variants when preparing initial fixtures. FE and BE remain separately built and deployed.
5. Run appropriate tests, record commands, results, file diffs, token usage and assumptions. Never claim unexecuted tests passed.
6. Do not introduce unimplemented refunds, inventory changes, durable persistence or distributed transaction guarantees.
7. Production deployment and destructive changes require human approval.
