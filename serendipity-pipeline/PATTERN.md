---
pattern_id: PL-5A7BDE31
name: Serendipity Pipeline
also_known_as: "Creative Autonomy, Cross-Domain Discovery"
layer: coordination
confidence: 0.85
status: draft
created: 2026-05-12
tags:
  - pattern-language
  - phase-16
  - coordination
  - coordination
---

# Serendipity Pipeline

## Also Known As
Creative Autonomy, Cross-Domain Discovery

## Problem
Knowledge organized by domain stays within domains. The most valuable insights come from unexpected connections between domains, but no systematic process produces these connections.

## Context
Any knowledge system spanning multiple domains: research vaults, cross-disciplinary teams, R&D organizations, innovation labs.

## Forces
Within-domain connections are easy to find but low novelty. Cross-domain connections are novel but hard to find. False connections waste attention; missed connections waste opportunity.

## Solution
Run a multi-stage serendipity pipeline: 1) discover cross-domain semantic bridges via TF-IDF or FAISS, 2) simulate counterfactuals on the causal graph to explore hypothetical relationships, 3) generate testable hypotheses using templates, 4) map consilience (reasoning pattern overlap), 5) sandbox-test each hypothesis for novelty, 6) present only those above a novelty threshold for human review. All outputs are Yellow-zone (pending human approval) by default.

## Resulting Context
Novel cross-domain insights are produced systematically. Most are noise (correctly filtered by sandbox), but the ones that survive are genuinely novel. The system's creativity is bounded by its knowledge graph — it cannot serendipitously discover what it does not already know.

## Examples
- [[06 System/Scripts/creative_serendipity.py]] — Creative_Serendipity
- [[06 System/Scripts/creative_counterfactual.py]] — Creative_Counterfactual
- [[06 System/Scripts/creative_discovery.py]] — Creative_Discovery
- [[06 System/Scripts/creative_cycle.py]] — Creative_Cycle



## Related Patterns
- **similar** → Activity-Dependent Selection: Both have selection thresholds: serendipity filters by novelty, ADSI by contribution
- **composes_into** → Distill-and-Publish: Serendipity produces creative outputs; Distill-and-Publish transforms them into artifacts


---
*Pattern from the SDEAS Phase 16 Pattern Language for Autonomous Systems.*
