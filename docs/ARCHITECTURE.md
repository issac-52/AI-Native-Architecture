# Architecture

## Idea
A business domain is a self-describing AI work unit containing executable code, contracts, invariants, tests and agent context. Co-location **does not** imply a single runtime or deployment.

## Conventional A
```text
baseline/
  backend/src/main/java/lab/baseline/{controller,service,repository,model}
  frontend/src/
```

## Domain-centered B
```text
domains/order/
  specification/{requirements,invariants,dependencies}.yaml
  contract/openapi.yaml
  backend/src/main/java/lab/ainative/order/
  frontend/OrderApp.jsx
  tests/java/lab/ainative/order/
  AGENTS.md
apps/api/    # Gradle source set points to the domain backend
apps/web/    # Vite imports the domain frontend
```

## Constraints
- Java and React compile/build independently; source co-location is not runtime coupling.
- Explicit domains, API contracts and dependency rules take precedence over folder proximity.
- Backend can still use hexagonal architecture and layered components **inside** a domain.
- Independent acceptance tests and enforceable CI checks are more reliable than agent-only instructions.
- Cross-domain workflows require explicit consistency and failure-handling design.

## Risks
UI/BE may not be 1:1; shared code has ambiguous ownership; very large domains may hurt context retrieval; Gradle/Vite require careful source-root wiring; semantic code search could reduce any benefit of physical grouping.

## Follow-up
Add multiple domains and independent contract tests, then measure identical agent work across layout and agent-instruction conditions separately.
