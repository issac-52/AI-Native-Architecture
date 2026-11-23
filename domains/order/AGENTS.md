# Order domain agent rules

Read specification/requirements.yaml, invariants.yaml, dependencies.yaml, contract/openapi.yaml.

Only this domain owns order behavior; apps/api and apps/web provide deployment/bootstrap code. Any API change requires checking backend, frontend, contract and tests. Do not invent payment, inventory, persistence or authentication behavior. Preserve idempotent cancellation and proper 400/404 errors. Run gradle :apps:api:test, python3 scripts/validate_architecture.py, and npm run build from apps/web. Do not edit independent evaluator-owned checks.
