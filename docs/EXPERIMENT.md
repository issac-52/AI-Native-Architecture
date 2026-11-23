# Reproducible A/B experiment

## Question
Does domain-centered FE/BE co-location help an autonomous AI agent implement end-to-end changes more reliably and efficiently than a conventional source layout?

## Setup and controls
1. Freeze a base SHA after both variants build and pass their existing tests.
2. Use identical model/version, permissions, tools, prompts, temperature (if applicable), hardware, token and time budgets.
3. Start each run in a fresh checkout. Randomize A/B run order and do not share intermediate agent work.
4. Run at least **three independent attempts per task per variant**; record unsuccessful runs, too.
5. Evaluate with **independent, hidden acceptance tests** that the implementation agent cannot rewrite.
6. Record model version, task, base SHA, prompt hash, tokens in/out, wall seconds, tool calls, regressions, cross-scope file changes and interventions.
7. Report distributions/medians, completion rates and uncertainty, rather than picking the best run.

## Metrics
Primary: independently verified task success. Secondary: test regressions, changes outside requested scope, token use, time and tool calls.

## Important confound
Variant B has explicit AGENTS.md and a spec. Compare layout alone separately from additional documentation: a later 2×2 design should toggle **layout** and **structured agent context** independently.

## Protocol
Run all initial tests -> prompt the same task from experiments/tasks.md -> save agent diff/logs -> run evaluator tests -> append one row in experiments/results-template.csv -> compare. A single-domain demo cannot measure cross-domain behavior.

## Threats
Small repository, uneven documentation, AI familiarity, caching, task ordering, flaky tools, non-independent test oracle and missing baseline parity. No empirical advantage is claimed before trials.
