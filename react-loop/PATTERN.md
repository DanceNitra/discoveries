---
pattern_id: PL-220253BF
name: ReAct Loop
also_known_as: "Observation-Thought-Action Cycle, Agentic Loop"
layer: coordination
confidence: 0.75
status: draft
created: 2026-05-12
tags:
  - pattern-language
  - phase-16
  - coordination
  - coordination
---

# ReAct Loop

## Also Known As
Observation-Thought-Action Cycle, Agentic Loop

## Problem
An agent with a single-shot response cannot handle multi-step tasks requiring external information, tool use, or iterative refinement.

## Context
Any agentic system that needs to interact with external tools, data sources, or environments to complete a task.

## Forces
Single-shot generation is fast but limited. Long chains of reasoning accumulate error. External state changes between turns.

## Solution
Structure each agent turn as a three-phase loop: Observe (read current state), Think (reason about next action), Act (execute tool call or produce output). After each Act, return to Observe. Terminate when goal is met or max iterations reached.

## Resulting Context
Agents can handle arbitrary-length tasks. Each turn is bounded and auditable. The loop supports tool use, error recovery, and human handoffs.

## Examples
- [[04 Resources/Concepts/ReAct Pattern.md]] — React Pattern
- [[04 Resources/Concepts/AI Agents.md]] — Ai Agents
- [[04 Resources/Concepts/Tool Calling.md]] — Tool Calling



---
*Pattern from the SDEAS Phase 16 Pattern Language for Autonomous Systems.*
