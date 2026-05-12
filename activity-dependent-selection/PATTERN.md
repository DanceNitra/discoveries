---
pattern_id: PL-5A875042
name: Activity-Dependent Selection
also_known_as: "ADSI, Integration-Validation Pipeline"
layer: validation
confidence: 0.8
status: draft
created: 2026-05-12
tags:
  - pattern-language
  - phase-16
  - validation
  - validation
---

# Activity-Dependent Selection

## Also Known As
ADSI, Integration-Validation Pipeline

## Problem
When new computational elements (neurons, agents, modules) are added to a system, they risk destabilizing existing function. The system must validate whether each new element contributes before committing resources.

## Context
Any system that adds new processing elements over time: neural networks adding units, biological neurogenesis, agent populations spawning new agents, vault notes being created.

## Forces
Adding new elements is necessary for growth but carries risk of disruption. Without a selection mechanism, the system either accepts everything (waste) or rejects everything (stasis). Validation must happen quickly and cheaply.

## Solution
Implement an integration-validation pipeline: specification, initialization, forward pass (measure contribution), backward pass (reinforce or withdraw support), survival criterion, and pruning. Elements that fail the survival criterion are removed.

## Resulting Context
The system grows organically with stable performance. New elements converge toward useful functions. Pruned elements are not wasted — they provide negative evidence that shapes future additions. The selection threshold must be tuned: too high stalls growth, too low accumulates noise.

## Examples
- [[04 Resources/Research/Neural Networks and Neurogenesis — Cross-Domain Synthesis.md]] — Neural Networks And Neurogenesis — Cross Domain Synthesis
- [[04 Resources/Concepts/Neural Networks.md]] — Neural Networks
- [[04 Resources/Concepts/Neuroplasticity.md]] — Neuroplasticity
- [[04 Resources/Concepts/Emergence.md]] — Emergence



## Related Patterns
- **composes_into** → Bounded Context for Agents: ADSI validates new agents; Bounded Context scopes them


---
*Pattern from the SDEAS Phase 16 Pattern Language for Autonomous Systems.*
