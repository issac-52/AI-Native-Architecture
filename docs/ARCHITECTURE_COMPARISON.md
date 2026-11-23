# Why this is not a simple seven-way architecture race

Architectures can address different design decisions and can be combined:

| Pattern | Design concern | Example combination |
|---|---|---|
| Feature-Sliced Design | Frontend layers and dependency direction | FSD + DDD backend |
| Domain-Driven Design | Language, models, bounded contexts | DDD + Hexagonal |
| Hexagonal | Application isolation via ports/adapters | Hexagonal + Modular Monolith |
| Vertical Slice | Use-case-specific organization | Slices within DDD context |
| Modular Monolith | Modules with explicit public boundaries in one deployment | Modular + DDD |
| AI-Native domain co-location | Context locality of FE/BE/spec/test for agent workflows | Co-location + any design above |
| Layered | Layer separation by technical responsibilities | Layers within bounded context |

## Three research questions

**1. Does path placement change deterministic full-file search time?** We used byte-identical files in seven synthetic directory layouts. The measured differences are tiny and do not represent AI speed.

**2. What does actual code organized under these styles look like to a lexical scanner?** We implemented independently runnable examples and record files/LOC/bytes/full-scan latency. These measurements are **confounded** by different implementations, differing code lengths and structure.

**3. Can an AI coding agent make more correct changes at lower cost?** Not measured. This requires a pinned model, consistent tools, fixed tasks, clean worktrees, repeated attempts, independent acceptance tests and real token/call logs.

## Publication rules

Do not rank architectural quality using source LOC or submillisecond timing. Do not call a Python lexical search an AI scan. Do not call synthetic path fixtures complete implementations of DDD or FSD. Link frozen source hashes, raw data, environment, tests and any failures.
