---
title: "Software Architecture Patterns as Agent Architecture"
date: 2026-05-15
layout: essay
slug: software-architecture-patterns-as-agent-architecture
---

# Software Architecture Patterns as Agent Architecture

# Software Architecture Patterns as Agent Architecture

> The thesis: Classical software architecture patterns — DDD's Bounded Contexts, Hexagonal's Ports & Adapters, Onion's Dependency Rule, EDA's Event Sourcing — are not metaphors or analogies for agent systems. They are **direct structural constraints** that solve the hard problems specific to autonomous agents: capability bleed, tool ambiguity, non-deterministic state drift, and safety surface erosion. An agent that violates these constraints is not "less elegant" — it is **structurally unsafe**.

| | |
|---|---|
| **Why this matters** | Agent systems fail in ways conventional software does not: hallucination cascades, tool-ambiguity loops, non-deterministic state drift, reward hacking. Classical architecture was designed to prevent a different set of failures (spaghetti coupling, untestable components, brittle deployment). But the two lists overlap more than is recognised. When an agent lacks bounded contexts, its capabilities bleed — the planner calls tools intended for the executor. When an agent lacks ports-and-adapters, every model swap requires reasoning-loop surgery. When an agent violates the dependency rule, safety surfaces depend on the subsystems they are meant to guard. This is not "engineering elegance"; this is **safety**. |
| **The core insight** | Every architectural constraint from classical software engineering maps to a **failure mode of autonomous systems**. The constraint is the cure. |

---

## 1. DDD Bounded Contexts → Agent Capability Boundaries

### The Classical Principle

> **Bounded Context**: A boundary around a domain model where every term has one unambiguous meaning. Within the context, the model is internally consistent. Across contexts, models may differ — translation happens at the boundary via anti-corruption layers.

From Domain-Driven Design (Evans, 2003): bounded contexts exist because the same word ("Customer", "Order", "Agent") means different things in different parts of the system. Trying to unify them universally creates models that are too complex for any single context to maintain.

### The Agent Failure

Agents develop (or are designed with) multiple capabilities that implicitly share state, terminology, and execution internals. The failure modes:

| Violation | What Happens | Real Hermes Example |
|---|---|---|
| **Planning-execution bleed** | The planner accesses tool execution internals to "optimise" tool calls — but violates the planner's abstraction of what tools are. | A planner that examines raw terminal output to tune args instead of treating tools as atomic operations. |
| **Memory-capability coupling** | The memory system knows about specific tool internals, creating a hidden dependency. If the tool changes, memory format breaks. | A session summary that assumes `read_file` returns line numbers, then breaks when `read_file` switches to JSON output. |
| **Safety-context coupling** | Guardrails have access to agent internals and become entangled with what they guard. | A safety monitor that can modify the tool permission table it's supposed to enforce. |

### Bounded Context Mapping for Agents

| Bounded Context            | Responsible For                                             | Owns                                                | Does NOT Own                                              | Translation Boundary                                                                                                              |
| -------------------------- | ----------------------------------------------------------- | --------------------------------------------------- | --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **Reasoning Context**      | Planning, tool selection, natural language output           | Conversation history, reasoning trace               | Tool execution, memory persistence, skill management      | Anti-corruption: reasoning sees only tool schemas and return types, never tool internals                                          |
| **Tool Execution Context** | Calling external functions, parsing results, error handling | Tool schemas, permission matrix, execution pipeline | Conversation meaning, task planning, user profile         | Anti-corruption: tool execution returns structured results, never modifies reasoning state                                        |
| **Memory Context**         | Persistence, retrieval, session management                  | Storage backends, indexing, search                  | Reasoning decisions, tool selection logic, skill matching | Translation: memory stores *facts* not *opinions* — reasoning can write "X caused Y" but memory stores it as a claim, not a truth |
| **Safety Context**         | Guardrails, escalation, permission enforcement              | Circuit breakers, alert rules, audit logs           

---

*Published through the SDEAS Epistemic Embodiment pipeline. Part of the vault's ongoing autonomous research program.*
