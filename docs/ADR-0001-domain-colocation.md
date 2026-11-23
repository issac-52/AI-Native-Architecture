# ADR-0001: Test domain-centered FE/BE co-location
- Date: 2026-11-23
- Status: **Experimental**

## Context
Autonomous coding agents must find code, understand impacts and validate changes. Technical-layer organization disperses one feature across directories.

## Decision
Create behaviorally equivalent A (layer-based Java + separate React) and B (order domain co-locates Java, React, specs and tests). Keep independent backend and frontend deployment.

## Alternatives
Separate repositories, ordinary monorepo, backend-only vertical slices, metadata-based code graph without physical co-location.

## Tradeoffs
Potentially simpler discovery and more explicit ownership versus multi-toolchain wiring, UI/BE boundary mismatches, cross-domain changes and expanding folder size.

## Revisit
After multi-task, multi-trial evaluation, and after introducing at least two interacting domains.
