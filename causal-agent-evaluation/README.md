# Causal Agent Evaluation

## Thesis

The **Fundamental Problem of Agent Evaluation** is that we can never observe the counterfactual: what would the agent have done under the *old* system given the same task? Traditional A/B testing on agents is confounded by task difficulty, selection bias in ground-truth evaluation, and heterogeneous treatment effects across agent architectures.

This library applies **causal inference** — Potential Outcomes Framework, Directed Acyclic Graphs (DAGs), do-calculus, and matching — to the problem of evaluating AI agent changes. It implements:

- **Matched-pair evaluation** (A/B with task pairs via propensity score matching)
- **Stratification by task difficulty** (blocking on confounders)
- **ATE estimation** with bootstrap confidence intervals
- **E-value sensitivity analysis** (how strong must unmeasured confounding be to explain away the result?)
- **DAG-based confounder check** (graphical criterion for backdoor adjustment)

## Origin

Scaffolded from causal-inference discovery: applying Potential Outcomes Framework to agent evaluation.

## Architecture

```
causal-agent-evaluation/
+-- README.md
+-- src/causal_agent_evaluation/
|   +-- __init__.py
|   +-- main.py
+-- docs/README.md
+-- tests/test_causal_agent_evaluation.py
+-- requirements.txt
```

## Getting Started

```bash
cd causal-agent-evaluation
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest
```
