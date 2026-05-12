---
pattern_id: PL-54105B08
name: Evergreen Lifecycle
also_known_as: "Seedling-to-Evergreen, Note Maturation"
layer: structure
confidence: 0.85
status: draft
created: 2026-05-12
tags:
  - pattern-language
  - phase-16
  - structure
  - structure
---

# Evergreen Lifecycle

## Also Known As
Seedling-to-Evergreen, Note Maturation

## Problem
Raw knowledge is captured in many forms — fleeting notes, research fragments, AI outputs. Without a maturation process, the knowledge base is a pile of unrefined material.

## Context
Any knowledge accumulation system: second brains, research vaults, documentation wikis, code comment databases.

## Forces
All captured knowledge has potential value, but most of it is raw. Premature organization wastes effort on material that will never be used. Without organization, valuable insights are lost in the noise.

## Solution
Define a lifecycle for each piece of knowledge: seedling (just captured, in inbox) → sprout (has links and some content) → evergreen (synthesized, connected, reviewed). Define promotion criteria: an evergreen must have 3+ incoming links, original synthesis beyond the source, and demonstrated usefulness. Run regular gap detection to find orphans and thin notes.

## Resulting Context
The knowledge base naturally converges toward high-quality, well-connected material. Most captured material stays at seedling/sprout level, which is fine — it is searchable but doesn't demand attention. The promotion criteria ensure that only genuinely valuable knowledge reaches evergreen status.

## Examples
- [[04 Resources/Concepts/Evergreen Notes.md]] — Evergreen Notes
- [[04 Resources/Concepts/Second Brain.md]] — Second Brain
- [[04 Resources/Concepts/Zettelkasten.md]] — Zettelkasten



## Related Patterns
- **composes_into** → Emergent Knowledge Graph: Evergreen lifecycle is the quality control layer for the emergent knowledge graph


---
*Pattern from the SDEAS Phase 16 Pattern Language for Autonomous Systems.*
