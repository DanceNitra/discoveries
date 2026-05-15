# Pattern Language for Autonomous Systems

A formal pattern catalogue for designing, describing, and evolving autonomous AI systems.

**18 patterns across 5 layers — discovered, extracted, and formalized by the SDEAS system itself.**

---

## Weekly Publications (2026-05-15)

Three new publications added from the SDEAS vault's Phase 18 Documentation Auto-Publish pipeline:

- **[Software Architecture Patterns as Agent Architecture](./docs/software-architecture-patterns-as-agent-architecture.md)** — How SOLID, DDD, hexagonal architecture, and design patterns map to autonomous AI agent design.
- **[The Disposition Effect as a Reinforcement Learning Failure](./docs/the-disposition-effect-as-a-reinforcement-learning-failure.md)** — A cross-domain synthesis: the behavioral finance disposition effect explained as a reinforcement learning failure mode.
- **[Neurobiology of Agent Memory Systems](./docs/neurobiology-of-agent-memory-systems.md)** — Hippocampal replay, synaptic consolidation, and their analogues in agent memory architectures.

---

## What This Is

These patterns were not written by a human architect. They were **discovered** by the SDEAS Phase 12 Creative Autonomy engine — a serendipity pipeline that finds non-obvious semantic bridges across domains — then **extracted and formalized** by Phase 16's pattern language system from the vault's 667+ evergreen notes spanning machine learning, neuroscience, software architecture, distributed systems, biology, and philosophy.

Each pattern follows the Christopher Alexander format: **name, problem, context, forces, solution, consequences, related patterns**.

---

## The Five Layers

### 🧠 Meta Layer (6 patterns)

How the system governs itself, learns, stays safe, and improves:

| Pattern | Problem It Solves | Origin |
|---------|------------------|--------|
| **Twin-and-Govern** | How to balance autonomy with human oversight | Phases 10-11 (Cognitive Twin + Adaptive Governance) |
| **Layered Guardrail** | Single safety checks have blind spots | Nine-Layer Guardrail Architecture note |
| **Crisis Circuit Breaker** | Failure cascades compound without detection | Phase 14 (adaptive_crisis_protocol.py, immune_system.py) |
| **Homeostatic Regulation** | Systems drift without continuous correction | Homeostasis.md, Control Theory.md |
| **Checkpoint-and-Resume** | Long-running processes are crash-vulnerable | Phase 14 (checkpoint_manager.py, fail_spiral_detector.py) |
| **Distill-and-Publish** | Internal knowledge is trapped without a publication pipeline | Phase 15 (epistemic_distiller.py, epistemic_builder.py) |

### 🏗️ Structure Layer (6 patterns)

How knowledge and agents are organized:

| Pattern | Problem It Solves | Origin |
|---------|------------------|--------|
| **Bounded Context for Agents** | Agent capabilities leak across boundaries | DDD ↔ Design Patterns discovery |
| **Pattern Compilation** | Reasoning from scratch every time is wasteful | Expertise.md, Chunking.md |
| **Emergent Knowledge Graph** | Rigid hierarchies resist cross-domain connections | Zettelkasten.md, Information Architecture.md |
| **Evergreen Lifecycle** | Raw knowledge needs a maturation pipeline | Second Brain.md, Evergreen Notes.md |
| **Gap-Driven Expansion** | Knowledge bases stagnate without gap detection | vault_gap_detector.py, vault_planner.py |

### 🔄 Coordination Layer (3 patterns)

How agents interact and work together:

| Pattern | Problem It Solves | Origin |
|---------|------------------|--------|
| **ReAct Loop** | Single-shot responses cannot handle multi-step tasks | ReAct Pattern.md |
| **Stigmergic Coordination** | Centralized coordination creates SPOFs | Swarm Intelligence.md, Stigmergy.md |
| **Serendipity Pipeline** | Within-domain knowledge misses cross-domain insights | Phase 12 (creative_cycle.py, creative_serendipity.py) |

### 📡 Communication Layer (1 pattern)

How components discover and invoke each other:

| Pattern | Problem It Solves | Origin |
|---------|------------------|--------|
| **Protocol-Mediated Discovery** | Static coupling prevents dynamic composition | MCP ↔ Message Queues discovery |

### ✅ Validation Layer (1 pattern)

How new elements survive integration:

| Pattern | Problem It Solves | Origin |
|---------|------------------|--------|
| **Activity-Dependent Selection** | New elements risk destabilizing existing function | ADSI discovery (Neural Networks ↔ Neurogenesis) |

---

## The Full Relationship Graph

```
                    META LAYER
                    ┌─────────────────────────────────────────────────┐
                    │                                                 │
  Cognitive Twin ──composes_into──→ Twin-and-Govern                  │
                   ↑                          │                      │
                   │                          │ refines              │
                   │                          ↓                      │
          ReAct Loop ←─────── Layered Guardrail                     │
               ↑                       ↑                            │
               │ composes_into          │ refined_by                 │
               │                       │                            │
  Homeostatic Regulation     Self-Modification Pipeline             │
               ↑                       │                            │
               │ refines               │ composes_into              │
  Crisis Circuit Breaker              ↓                            │
                            Pattern Compilation ──prerequisite──→   │
                   │                              │                 │
  Distill-and-Publish ←───────────── Twin-and-Govern               │
        ↑                    ↑                                      │
        │ composes_into      │ composes_into                       │
        │                    │                                      │
  Emergent Knowledge Graph  Serendipity Pipeline ←── similar ── ADSI│
        ↑                    │                                      │
        │ prerequisite       │ composes_into                       │
        │                    ↓                                      │
  Gap-Driven Expansion Distill-and-Publish                         │
        │                                                           │
        │ composes_into                                             │
        ↓                                                           │
  Evergreen Lifecycle                                               │
        │                                                           │
        │ composes_into                                             │
        ↓                                                           │
  Emergent Knowledge Graph                                          │
                    └─────────────────────────────────────────────────┘

                    STRUCTURE LAYER
                    ┌───────────────────────────────────────────────┐
                    │                                               │
  Pattern Compilation ──prerequisite──→ Bounded Context for Agents │
                                               │                    │
                                               │ prerequisite       │
                                               ↓                    │
                                     Stigmergic Coordination        │
                                           ↕  alternative            │
                                     Protocol-Mediated Discovery    │
                    └───────────────────────────────────────────────┘

                    COORDINATION LAYER
                    ┌───────────────────────────────────────────────┐
                    │                                               │
  ReAct Loop ← composes_into ← Homeostatic Regulation             │
  ReAct Loop ← composes_into ← Checkpoint-and-Resume              │
                    │                                               │
  Serendipity Pipeline (creative autonomy)                         │
       │ similar                                                    │
       ↓                                                            │
  Activity-Dependent Selection (validation)                        │
                    └───────────────────────────────────────────────┘
```

---

## What the System Says About Itself

Every SDEAS phase is described by one or more patterns from this catalogue:

| Phase | Pattern(s) |
|-------|-----------|
| 1-2 Retention & Expansion | Evergreen Lifecycle, Gap-Driven Expansion, Emergent Knowledge Graph |
| 3-6 Autonomous Generation & Infrastructure | Checkpoint-and-Resume, Crisis Circuit Breaker, Self-Modification Pipeline |
| 7-9 Agentic & Emergent Architecture | ReAct Loop, Bounded Context for Agents, Stigmergic Coordination, Protocol-Mediated Discovery |
| 10-11 Cognitive Replication & Adaptive Governance | Cognitive Twin, Twin-and-Govern, Layered Guardrail |
| 12 Creative Autonomy | Serendipity Pipeline, Activity-Dependent Selection |
| 13 Recursive Meta-Architecture | Gap-Driven Expansion, Evergreen Lifecycle |
| 14 Resilience Engine | Crisis Circuit Breaker, Checkpoint-and-Resume |
| 15 Epistemic Embodiment | Distill-and-Publish |
| 16 Pattern Language | Pattern Compilation |

---

## How These Patterns Were Discovered

1. **Phase 12 Creative Autonomy** — The serendipity engine found cross-domain semantic bridges (Neural Networks ↔ Neurogenesis → ADSI, DDD ↔ Design Patterns → Bounded Context, Swarm ↔ MAS → Stigmergic Coordination, MCP ↔ Message Queues → Protocol-Mediated Discovery)

2. **Phase 15 Epistemic Embodiment** — Each bridge was distilled into an essay publication, scaffolded into a GitHub-ready artifact, and pushed to the `discoveries` repo

3. **Phase 16 Pattern Language** — The four discoveries revealed a hidden stack (validation → structure → coordination → communication → meta). Six more patterns were extracted from the vault's existing evergreen notes and scripts. Six more followed, covering the remaining SDEAS phases. The result is an 18-pattern catalogue that describes the entire autonomous system that produced it.

---

## How to Use This Catalogue

### For Designers
When building an autonomous AI system, use the pattern graph as a checklist:
1. Start with **ReAct Loop** for the agent loop
2. Add **Bounded Context for Agents** to scope capabilities
3. Choose **Stigmergic Coordination** or **Protocol-Mediated Discovery** for inter-agent communication
4. Wrap in **Layered Guardrail** for safety and **Twin-and-Govern** for autonomy boundaries
5. Add **Checkpoint-and-Resume** and **Crisis Circuit Breaker** for resilience
6. Apply **Emergent Knowledge Graph** + **Evergreen Lifecycle** + **Gap-Driven Expansion** for knowledge
7. Add **Serendipity Pipeline** for creative insight generation
8. Close the loop with **Distill-and-Publish** for external impact

### For Researchers
Each pattern's problem-context-forces-solution structure provides a formal hypothesis:
- If the solution is applied, the consequences should follow
- If the forces change, the solution may need adaptation
- The relationship links encode testable composition rules

### For the SDEAS System Itself
The pattern language is self-describing — `Pattern Compilation` describes how these patterns themselves were discovered and compiled. The catalogue can be extended by running the serendipity pipeline on new vault content and extracting the resulting patterns.

---

## Repository Structure

```
discoveries/
├── README.md                        # This file
├── activity-dependent-selection/    # ADSI — validation
├── bounded-context-for-agents/      # DDD → agent capability scoping
├── checkpoint-and-resume/           # Session persistence
├── cognitive-twin/                  # User model + reasoning mirror
├── crisis-circuit-breaker/          # Fail-spiral containment
├── ddd-design-patterns/             # Original discovery artifact
├── distill-and-publish/             # Knowledge → publication pipeline
├── emergent-knowledge-graph/        # Zettelkasten + wikilinks
├── evergreen-lifecycle/             # Seedling → sprout → evergreen
├── gap-driven-expansion/            # Blind-spot detection + auto-fill
├── homeostatic-regulation/          # Negative feedback loops
├── layered-guardrail/               # Defense-in-depth safety
├── mcp-message-queues/              # Original discovery artifact
├── pattern-compilation/             # Expertise encoding
├── protocol-mediated-discovery/     # Runtime schema negotiation
├── react-loop/                      # Observe-Think-Act
├── self-modification-pipeline/      # Bounded auto-evolution
├── serendipity-pipeline/            # Creative autonomy
├── stigmergic-coordination/         # Environment-mediated coordination
├── swarm-mas/                       # Original discovery artifact
└── twin-and-govern/                 # Cognitive twin + governance gate
```

---

*Generated by SDEAS Phase 16 — Pattern Language for Autonomous Systems.*  
*Built on Phase 12 (Creative Autonomy) + Phase 15 (Epistemic Embodiment).*  
*Rooted in the vault: 667+ notes, 6,867 causal edges, FAISS semantic index, 18 published patterns.*
