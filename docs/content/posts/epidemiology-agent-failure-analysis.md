---
layout: post
title: "Epidemiology × Agent Failure Analysis"
date: 2026-05-16
categories: [cross-domain, agents, reliability]
---

# Epidemiology × Agent Failure Analysis

**Agent failures are diseases in a population of sessions.**
Epidemiology studies disease distribution in populations. Agent failure analysis
studies error distribution in session populations. The methods are structurally identical.

## The Core Mapping

| Epidemiological Concept | Agent Equivalent |
|---|---|
| Incidence | Rate of new failures per session |
| Prevalence | Fraction of active sessions in error state |
| Outbreak | Error rate > 3 sigma above baseline |
| Epidemic curve | Time series of error events |
| Cohort study | Compare two agent variants side-by-side |
| Case-control | Compare failed vs successful sessions retroactively |
| Survival analysis | How long until a session crashes (Kaplan-Meier) |
| Confounding | Task difficulty confounds agent A/B tests |
| Berkson's bias | Bug reports overrepresent multi-error sessions |

## Why This Matters

Current agent debugging is **clinical medicine** — single-patient diagnosis.
Epidemiology is **public health** — population-level pattern detection.

When your agent fleet has an error spike, you need:
1. A **case definition** — what counts as a failure?
2. An **epidemic curve** — is this point-source or propagated?
3. **Attack rate** — what fraction of sessions are affected?
4. **Stratified analysis** — which agent version, tool, or prompt is the risk factor?

## Practical Takeaway

Stop debugging single sessions. Start doing epidemiology on your agent logs.
The next time your agent system has a mysterious error spike, ask: what is the
incidence? What is the attack rate? What is the risk ratio between your old
prompt and your new one?

---
*Cross-domain vault synthesis. Sources: Epidemiology.md, Agent Observability.md,
Agent Evaluation.md, Agent Safety & Guardrails.md, Survival Analysis.md.*
