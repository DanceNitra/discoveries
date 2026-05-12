---
pattern_id: PL-D9931BE9
name: Cognitive Twin
also_known_as: "User Model, Reasoning Mirror"
layer: meta
confidence: 0.85
status: draft
created: 2026-05-12
tags:
  - pattern-language
  - phase-16
  - meta
  - meta
---

# Cognitive Twin

## Also Known As
User Model, Reasoning Mirror

## Problem
An autonomous system needs to act on behalf of a human, but without a model of how that human thinks, the system cannot predict what the human would approve or object to.

## Context
Any AI system that makes decisions a human would otherwise make: coding agents, research assistants, writing assistants, governance filters.

## Forces
A good model of the user enables accurate delegation. An inaccurate model produces misaligned outputs. Building the model requires observing the user, which is expensive and potentially privacy-invasive.

## Solution
Build a cognitive twin by ingesting session transcripts and extracting reasoning patterns (deduction, analogy, synthesis, etc.). Track acceptance rates per pattern type. Maintain a causal model of the user's knowledge domain. On each decision, the twin generates a reasoning trace in the user's style and an objection prediction. Score the twin's accuracy against actual user decisions and update pattern weights recursively.

## Resulting Context
The system increasingly makes decisions the user would make. Objection predictions catch potential disagreements before they happen. The twin requires ongoing calibration — the user's thinking evolves, and the twin must evolve with it. Without recursion, the twin becomes stale.

## Examples
- [[06 System/Scripts/cognitive_twin_agent.py]] — Cognitive_Twin_Agent
- [[06 System/Scripts/cognitive_pattern_miner.py]] — Cognitive_Pattern_Miner
- [[06 System/Scripts/cognitive_causal_model.py]] — Cognitive_Causal_Model
- [[06 System/Scripts/cognitive_objection_predictor.py]] — Cognitive_Objection_Predictor



## Related Patterns
- **composes_into** → Twin-and-Govern: Cognitive twin is the model layer; Twin-and-Govern adds the governance gate
- **composes_into** → ReAct Loop: The twin's reasoning traces inform the ReAct loop's thinking phase


---
*Pattern from the SDEAS Phase 16 Pattern Language for Autonomous Systems.*
