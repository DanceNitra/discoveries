---
pattern_id: PL-9F163DFC
name: Protocol-Mediated Discovery
also_known_as: "Runtime Schema Negotiation"
layer: communication
confidence: 0.8
status: draft
created: 2026-05-12
tags:
  - pattern-language
  - phase-16
  - communication
  - communication
---

# Protocol-Mediated Discovery

## Also Known As
Runtime Schema Negotiation

## Problem
In agentic systems, agents need to discover and invoke each other's capabilities at runtime. Static interfaces assume compile-time knowledge, which fails when agents are dynamically spawned.

## Context
Systems where agents, tools, or services appear and disappear dynamically. LLM-based systems where the agent must discover what tools are available at inference time.

## Forces
Static coupling prevents dynamic composition. Runtime discovery adds latency and potential failure points. Agents must be able to discover capabilities without human configuration.

## Solution
Use a lightweight protocol where capabilities are described by schema (JSON Schema or similar) and discovered via a registry at runtime. The agent negotiates capability use through the protocol rather than through hardcoded calls.

## Resulting Context
High flexibility: tools can be added, removed, or versioned without reconfiguring agents. Latency increases slightly per discovery. Schema drift must be handled (version negotiation or backward compatibility).

## Examples
- [[04 Resources/Concepts/Model Context Protocol (MCP).md]] — Model Context Protocol (Mcp)
- [[04 Resources/Concepts/REST.md]] — Rest
- [[04 Resources/Concepts/gRPC.md]] — Grpc



## Related Patterns
- **prerequisite** → Bounded Context for Agents: Agents need a protocol to discover boundaries before they can be bounded


---
*Pattern from the SDEAS Phase 16 Pattern Language for Autonomous Systems.*
