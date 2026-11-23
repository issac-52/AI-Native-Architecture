# Runnable architecture profiles (v0.3)

Six independently executable Spring Boot applications implement the **same** order HTTP contract; one FSD frontend is independently built and can target any backend.

| Variant | Gradle run task | Port | Distinct design element |
|---|---|---:|---|
| Layered | `gradle :baseline:backend:bootRun` | 8081 | Controller → service → repository |
| AI-Native | `gradle :apps:api:bootRun` | 8080 | FE/BE/contract/spec/test owned by one domain |
| DDD | `gradle :variants:ddd:bootRun` | 8082 | Order aggregate + domain repository abstraction |
| Hexagonal | `gradle :variants:hexagonal:bootRun` | 8083 | Framework-free domain/service with inbound/outbound ports and adapters |
| Vertical Slice | `gradle :variants:vertical-slice:bootRun` | 8084 | Separate create, list and cancel handlers |
| Modular Monolith | `gradle :variants:modular-monolith:bootRun` | 8085 | OrderFacade module API, hidden implementation |

React apps: conventional `baseline/frontend` (port 5174), AI-Native `apps/web` (5173), FSD `variants/fsd-web` (5175). From each app directory run `npm install && npm run dev`. FSD defaults to backend 8081; use `API_TARGET=http://localhost:8082 npm run dev` on Unix to target DDD. On Windows PowerShell, set `$env:API_TARGET="http://localhost:8082"` first.

## Shared behavior and independent validation

- `POST /api/orders` -> 201, `{id,productName,quantity,status:"CREATED"}`.
- `GET /api/orders` -> 200, orders sorted by ID.
- `POST /api/orders/{id}/cancel` -> 200, status CANCELLED, safe to repeat.
- Invalid payload -> 400, unknown order ID -> 404.
- Every server stores orders in memory; restarting it resets state.

Each Java variant inherits the same JUnit HTTP suite in `benchmarks/contract-tests/src/test/java/lab/contract/OrderContractSuite.java`.

```bash
gradle :baseline:backend:test :apps:api:test :variants:ddd:test :variants:hexagonal:test :variants:vertical-slice:test :variants:modular-monolith:test
python3 scripts/validate_boundaries.py
python3 scripts/benchmark_runnable.py --repeats 100 --output results/local-runnable
```

The three React apps have separate Vite production builds in GitHub Actions.

## Scope restrictions

This is a **small single-business-domain teaching example**. DDD uses a simplified aggregate. Hexagonal uses only one persistence adapter. The modular monolith demonstrates one encapsulated module, not independently verified intermodule collaboration. FSD implements app/pages/features/entities/shared with public entry points; import linting is only a partial architectural check. None of these implementations represent every feature or performance characteristic of the corresponding methodology.

**The same HTTP contract demonstrates basic functional parity, not identical internals or complete architecture conformance.**

## Evidence

- [Identical-code layout measurements](../results/latest/RESULTS.md): 7 profiles with the same seven source files; directory paths differ.
- [Runnable-source measurements](../results/runnable/RESULTS.md): 7 profile compositions with their actual source code; code size and structure differ.
- [Raw runnable observations](../results/runnable/raw.csv), [machine-readable summary](../results/runnable/summary.json), [SVG charts](../results/runnable/scan_latency.svg).
- [AI-agent evaluation protocol](EXPERIMENT.md): real agent task success/token measurement **not yet performed**.
