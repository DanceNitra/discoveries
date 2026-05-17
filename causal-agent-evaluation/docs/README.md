# Causal Agent Evaluation — Documentation

---
title: Causal Inference for AI Agent Evaluation
type: publication
format: library
source_type: discovery
source_id: DISC-CAEEVAL01
novelty: 0.85
value_alignment: 0.95
status: draft
created: 2026-05-15
tags:
  - causal-inference
  - agent-evaluation
  - potential-outcomes
  - matching
  - phase-15
---

## Concepts

### Fundamental Problem of Agent Evaluation
We can never observe the counterfactual outcome for the same agent under a different system configuration. This is isomorphic to the Fundamental Problem of Causal Inference (Holland, 1986).

### Confounding by Task Difficulty
Harder tasks naturally produce lower scores. If task difficulty is correlated with treatment assignment (e.g., we test the new agent on easier tasks), the naive ATE is biased.

### Selection Bias in Ground-Truth Evaluation
Ground-truth evaluators may selectively label tasks they are confident about, creating non-random missingness.

### Ablation Studies with do-calculus
The do-operator (Pearl, 2009) formalises intervention: P(Y | do(Treatment)) vs P(Y | Treatment). Ablation studies in agent evaluation are do-calculus operations — we intervene on the component being ablated.

### Heterogeneous Treatment Effects
Different agent architectures respond differently to the same change. Conditional ATE (CATE) by difficulty stratum reveals this.

## API

### `CausalAgentEvaluator`

```python
evaluator = CausalAgentEvaluator(random_seed=42)

# Matched-pair evaluation
result = evaluator.matched_pair_evaluation(
    treatment_scores=[0.85, 0.78, ...],
    control_scores=[0.72, 0.80, ...],
    covariates={"task_difficulty": [3, 5, ...]}
)

# Stratified ATE
stratified = evaluator.stratified_ate(
    treatment_scores, control_scores,
    strata_labels=["easy", "hard", ...]
)

# E-value sensitivity
e_value = evaluator.e_value(ate=0.10, ci_lower=0.02)

# DAG confounder check
dag_result = evaluator.check_backdoor_criterion(
    dag_edges=[("task_difficulty", "treatment"), ...],
    treatment="treatment",
    outcome="agent_score"
)
```
