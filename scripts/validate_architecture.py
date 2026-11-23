#!/usr/bin/env python3
"""Required file checks; functional tests and semantic boundary rules are separate."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
required = [
    "AGENTS.md", "docs/ARCHITECTURE.md", "docs/EXPERIMENT.md",
    "domains/order/AGENTS.md", "domains/order/specification/requirements.yaml",
    "domains/order/specification/invariants.yaml", "domains/order/specification/dependencies.yaml",
    "domains/order/contract/openapi.yaml", "domains/order/backend/src/main/java/lab/ainative/order/OrderController.java",
    "domains/order/frontend/OrderApp.jsx", "apps/api/build.gradle", "apps/web/package.json",
    "baseline/backend/build.gradle", "baseline/frontend/package.json",
    "benchmarks/contract-tests/src/test/java/lab/contract/OrderContractSuite.java",
    "variants/ddd/build.gradle", "variants/hexagonal/build.gradle",
    "variants/vertical-slice/build.gradle", "variants/modular-monolith/build.gradle",
    "variants/fsd-web/package.json", "scripts/benchmark_discovery.py",
    "scripts/benchmark_runnable.py", "scripts/validate_boundaries.py",
]
missing = [item for item in required if not (root / item).is_file()]
for item in required:
    print(("FAIL" if item in missing else "PASS"), item)
if missing:
    raise SystemExit(f"{len(missing)} required files missing")
print("PASS file-structure smoke checks")
