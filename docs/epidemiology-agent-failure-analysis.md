---
title: "Epidemiology × Agent Failure Analysis"
date: 2026-05-17
layout: essay
slug: epidemiology-agent-failure-analysis
---

# Epidemiology × Agent Failure Analysis

# Epidemiology × Agent Failure Analysis

> **Agent failures are diseases in a population of sessions.** Every agent system — whether a single CLI agent or a fleet of production agents — generates a stream of events (tool calls, errors, crashes, loops) across a population of sessions. These events have incidence rates, incubation periods, transmission dynamics, and risk factors. Epidemiology provides a mature, 200-year-old toolkit for studying exactly this kind of data. This bridge synthesises the two domains into a unified framework: **epidemiological agent failure analysis**.

---

## 1. Thesis: Why Epidemiology for Agents?

Standard agent debugging is **clinical medicine** — a single patient (session) presents with symptoms (error), and the developer diagnoses the cause. This works for individual failures but misses systemic patterns.

Epidemiology is **public health** — it studies disease at the population level. Instead of asking "why did this session crash?", epidemiology asks:

| Clinical Question | Epidemiological Question | Translation for Agents |
|---|---|---|
| Why did *this* session fail? | What is the *incidence rate* of failures? | How many sessions fail per 100 runs? |
| What tool caused the error? | What are the *risk factors* for failure? | Which tools, prompts, or model versions predict errors? |
| How do I fix this bug? | What interventions *prevent* failures? | Which guardrails reduce error rates? |
| This session crashed after 50 turns | What is the *survival function* of sessions? | How long do sessions live before crashing? |

**The core insight**: agent telemetry data (session logs, tool calls, error events, latency spans) is structurally identical to epidemiological surveillance data. The same methods that detect disease outbreaks in populations detect error cascades in agent systems.

---

## 2. Mapping Epidemiology onto Agent Failure Data

### 2.1 Core Quantities

| Epidemiological Quantity | Agent Equivalent | How to Measure |
|---|---|---|
| **Population** | All agent sessions (or all turns within sessions) | Session ID registry or log stream |
| **Case** | A session meeting failure criteria (crash, loop, safety violation, hallucination) | Operational definition with inclusion/exclusion criteria |
| **Incidence** | Rate of new failures in a time period | `new failures / sessions started` per hour |
| **Prevalence** | Fraction of currently active sessions that are failed | `ongoing failures / active sessions` at a point in time |
| **Person-time** | Session-time at risk | Sum of (elapsed seconds across all active sessions) |
| **Incidence rate** | Failures per unit of session-time | `new failures / total session-seconds` |
| **Attack rate** | Proportion of sessions that fail in an "outbreak" period | `failures in period / sessions started in period` |
| **Mortality rate** | Sessions that crash-terminate (vs recover) | `crashes / total sessions` |
| **Case fatality rate** | Proportion of failed sessions that result in crash | `crashes / failures` |

### 2.2 Study Designs for Agent Comparisons

| Design | When to Use | How to Execute |
|---|---|---|
| **Cohort study** | Compare two agent variants side-by-side | Run Agent v1 and Agent v2 on same task pipeline for N days; measure failure incidence in each |
| **Case-control study** | Investigate rare failure modes | Collect all "session crashed" events (cases) + random sample of healthy sessions (controls); look backward at prompt complexity, tool chain length, model version |
| **Cross-sectional** | Snapshot of current system health | Sample all active sessions at 3 PM; measure fraction in error state, loop state, healthy state |
| **RCT (A/B test)** | Gold standard for intervention efficacy | Randomize user traffic to Agent A (control) vs Agent B (treatment); measure task success rate, cost, safety violations |
| **Crossover trial** | Compare within same session population | Run Agent A for 1 hour, then Agent B for 1 hour, alternating; controls for time-of-day effects |
| **N-of-1 trial** | Optimize a single long-running agent | Modify one parameter per session; track metrics across sessions to find optimum |

---

## 3. Incidence, Prevalence, and Error Accumulation

### 3.1 Incidence Types

| Type | Definition | Agent Application |
|---|---|---|
| **Cumulative incidence** | Proportion of sessions that fail within a fixed window (e.g., first N turns) | "12% of sessions encounter a tool timeout in the first 10 turns" |
| **Incidence rate** | Failures per unit of session runtime | "0.03 errors per minute of agent operation" |
| **Attack rate** | Proportion of sessions affected during a specific incident | "40% of sessions initiated during the model outage failed" |

### 3.2 The Incidence–Prevalence Relationship

```
Prevalence ≈ Incidence × Average Duration of Error
```

This epidemiological identity has direct consequences for error management:

| Scenario | What's Happening | Fix |
|---|---|---|
| **High incidence, low duration** |

---

*Published through the SDEAS Epistemic Embodiment pipeline. Part of the vault's ongoing autonomous research program.*
