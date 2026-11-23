#!/usr/bin/env python3
"""Checks a small subset of architectural dependency rules; not a full Java parser."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors = []


def java_files(relative):
    return list((ROOT / relative).rglob("*.java"))


# In Hexagonal, neither domain nor application should import Spring or adapters.
for folder in [
    "variants/hexagonal/src/main/java/lab/hexagonal/domain",
    "variants/hexagonal/src/main/java/lab/hexagonal/application",
]:
    for file in java_files(folder):
        for line in file.read_text().splitlines():
            if line.strip().startswith("import "):
                if "org.springframework" in line or "lab.hexagonal.adapter" in line:
                    errors.append(f"{file.relative_to(ROOT)}: inward dependency violated: {line}")

# DDD model cannot import Spring or outer adapters.
for file in java_files("variants/ddd/src/main/java/lab/ddd/order/domain"):
    for line in file.read_text().splitlines():
        if line.strip().startswith("import ") and (
            "org.springframework" in line or "lab.ddd.order.infrastructure" in line
        ):
            errors.append(f"{file.relative_to(ROOT)}: domain depends on framework/adapter")

# A modular monolith consumer must not import order internals.
for file in java_files("variants/modular-monolith/src/main/java/lab/modular/web"):
    if "import lab.modular.order.internal." in file.read_text():
        errors.append(f"{file.relative_to(ROOT)}: import of hidden module internals")

# FSD: lower layers may not reference upper layers; this is a shallow source-path rule.
root = ROOT / "variants/fsd-web/src"
for layer, forbidden in {
    "shared": ("../features", "../entities", "../pages", "/features/", "/entities/", "/pages/"),
    "entities": ("../features", "../pages", "/features/", "/pages/"),
    "features": ("../pages", "/pages/"),
}.items():
    for file in (root / layer).rglob("*"):
        if file.suffix not in {".js", ".jsx", ".ts", ".tsx"}:
            continue
        for line in file.read_text().splitlines():
            if ("import " in line or "from " in line) and any(term in line for term in forbidden):
                errors.append(f"{file.relative_to(ROOT)}: FSD upward dependency: {line}")

if errors:
    for error in errors:
        print("FAIL", error)
    raise SystemExit(1)
print("PASS: checked hexagonal, DDD, modular and FSD dependency constraints")
