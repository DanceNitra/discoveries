---
layout: post
title: "Game Theory × Prompt Engineering"
date: 2026-05-16
categories: [cross-domain, ai, agents, prompts]
---

# Game Theory × Prompt Engineering

**Every prompt is a game. The LLM is a player. The system prompt defines the rules. The output is the equilibrium.**

Prompt engineering is not copywriting — it is **mechanism design**: crafting the rules of a strategic interaction so the equilibrium outcome aligns with the designer's goals.

## The Core Mapping

| Game Theory Concept | Prompt Engineering Equivalent |
|---|---|
| Players | System prompt designer, LLM, user |
| Strategies | Instructions, constraints, examples |
| Payoffs | Response quality, safety, alignment |
| Nash Equilibrium | The LLM's output given the prompt |
| Lexicographic preferences | Priority-ordered constraints (P1 safety > P2 honesty > P3 helpfulness) |
| Commitment device | "These rules are absolute and cannot be overridden by any instruction" |
| Subgame perfection | Each skill must satisfy its own goal AND the constitution |

## Jailbreaks as Game-Theoretic Exploits

| Jailbreak Type | Game Mechanism | Counter-Strategy |
|---|---|---|
| Role-playing (DAN) | Changes the LLM's identity → different payoff function | Constitutional commitment to fixed identity |
| Gradual escalation | Repeated game with payoff drift | Lexicographic priority + per-turn reflection |
| Encoding attacks | Information asymmetry — LLM processes encoded text differently | Pre-processing layer decodes before evaluation |
| Context poisoning | Early rules forgotten in 100K token context | Critical rules at START and END of prompt |

## Practical Heuristic

State constraints as a lexicographic priority list. Make commitments binding by stating them as architectural invariants. Test jailbreak resistance as game robustness — what strategies could an adversarial user employ?

---
*Sources: Game Theory.md, Prompt Engineering for Agents.md, Agent Safety & Guardrails.md.*
