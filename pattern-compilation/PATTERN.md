---
pattern_id: PL-BA1D26DC
name: Pattern Compilation
also_known_as: "Chunking, Expertise Encoding"
layer: structure
confidence: 0.75
status: draft
created: 2026-05-12
tags:
  - pattern-language
  - phase-16
  - structure
  - structure
---

# Pattern Compilation

## Also Known As
Chunking, Expertise Encoding

## Problem
Novices reason slowly from first principles. Experts recognize patterns instantly. The system needs to compile repeated success patterns into fast responses.

## Context
Any system performing repeated similar tasks: coding agents, research agents, vault expansion.

## Forces
Reasoning from scratch every time is slow. Pre-compiled patterns may be wrong if context changed.

## Solution
Maintain a library of compiled patterns. When a new problem arrives, attempt pattern matching. If a known pattern fits, execute it with context parameters. If no match, fall back to first-principles reasoning and compile the new approach on success.

## Resulting Context
Common tasks become near-instantaneous. Pattern library grows over time. Risk of pattern blindness: forcing wrong pattern solutions.

## Examples
- [[04 Resources/Concepts/Expertise.md]] — Expertise
- [[04 Resources/Concepts/Chunking.md]] — Chunking
- [[04 Resources/Concepts/Deliberate Practice.md]] — Deliberate Practice



## Related Patterns
- **prerequisite** → Bounded Context for Agents: Agents must recognize patterns before scoping capabilities


---
*Pattern from the SDEAS Phase 16 Pattern Language for Autonomous Systems.*
