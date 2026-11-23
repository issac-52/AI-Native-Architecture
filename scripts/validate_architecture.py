#!/usr/bin/env python3
"""Structural smoke checks only; execute Java tests and web builds separately."""
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]
files = [
    'AGENTS.md', 'docs/ARCHITECTURE.md', 'docs/EXPERIMENT.md',
    'domains/order/AGENTS.md', 'domains/order/specification/requirements.yaml',
    'domains/order/specification/invariants.yaml',
    'domains/order/specification/dependencies.yaml', 'domains/order/contract/openapi.yaml',
    'domains/order/backend/src/main/java/lab/ainative/order/OrderController.java',
    'domains/order/frontend/OrderApp.jsx', 'apps/api/build.gradle',
    'apps/web/package.json', 'baseline/backend/build.gradle',
    'baseline/frontend/package.json',
]
missing = [file for file in files if not (root / file).is_file()]
for file in files:
    print(('FAIL' if file in missing else 'PASS'), file)
if missing:
    sys.exit(f'{len(missing)} required files missing')
print('Structural validation passed; runtime tests are separate.')
