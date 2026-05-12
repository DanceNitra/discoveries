---
pattern_id: PL-073505D6
name: Gap-Driven Expansion
also_known_as: "Knowledge Growth Engine, Auto-Expansion"
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

# Gap-Driven Expansion

## Also Known As
Knowledge Growth Engine, Auto-Expansion

## Problem
Knowledge bases have blind spots — missing concepts, weak connections, orphan notes. Without systematic gap detection, these blind spots persist and the knowledge base becomes stagnant.

## Context
Any growing knowledge system: research vaults, documentation, learning curricula, corporate wikis.

## Forces
Gaps are invisible by definition — the system does not know what it does not know. Manual gap detection is slow and inconsistent. Automated gap detection requires a baseline of "healthy" to compare against.

## Solution
Periodically scan the knowledge base for measurable gaps: orphan notes (zero backlinks), thin notes (below minimum content threshold), broken links, low link density, isolated clusters, missing crosslinks (topics mentioned in one note but not linked to an existing note). Prioritize gaps by impact (most-linked orphans highest). Queue the top gaps for automated research and synthesis. After expansion, re-scan to verify gaps closed.

## Resulting Context
The knowledge base grows toward completeness systematically. The gap detection metrics provide a health score that trends upward. Some gaps are intentional (concepts not yet added) — the system must distinguish between true gaps and intentionally empty territory.

## Examples
- [[06 System/Scripts/vault_gap_detector.py]] — Vault_Gap_Detector
- [[06 System/Scripts/vault_planner.py]] — Vault_Planner
- [[04 Resources/Concepts/Information Architecture.md]] — Information Architecture



## Related Patterns
- **composes_into** → Evergreen Lifecycle: Gap detection feeds the evergreen lifecycle with candidates for creation/promotion
- **prerequisite** → Emergent Knowledge Graph: The knowledge graph must exist before gaps can be detected within it


---
*Pattern from the SDEAS Phase 16 Pattern Language for Autonomous Systems.*
