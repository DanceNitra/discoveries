# Neural Networks and Neurogenesis — Cross-Domain Synthesis

A cross-domain framework describing how artificial neural networks and biological neurogenesis share isomorphic computational principles.

## Overview

This project emerges from an autonomous creative cycle in the SDEAS vault. Two notes from distant domains — **Neural Networks** (machine learning) and **Neurogenesis** (developmental neuroscience) — were found to share a latent structural relationship by the Phase 12 Serendipity Engine.

**Serendipity Score: 0.950 | Novelty: 0.9 | Value Alignment: 0.98**

## The Core Insight

Both artificial neural networks and biological neurogenesis implement what we call **Activity-Dependent Selective Integration** (ADSI) — a process where new computational elements survive only if they contribute to overall system function:

| Phase | Neural Networks | Neurogenesis |
|-------|----------------|--------------|
| Specification | Architecture defines layer structure | Gene expression specifies progenitor cell type |
| Initialization | Random weights (Xavier/He) | Stochastic migration + initial synaptic targets |
| Forward pass | Info propagates; if output degrades, unit pruned | New neurons receive input; if they depolarize coherently, they survive |
| Backward pass | Gradient flows → large gradient = important | BDNF signaling → promotes survival of active neurons |
| Survival criterion | Validation loss decreases | Successful synaptic integration |
| Pruning trigger | Weight magnitude → 0 (regularization) | Failure to receive trophic support → apoptosis |

## Structure

```
adsi/
├── README.md
├── src/adsi_core/
│   ├── __init__.py
│   └── core.py            # ActivityDependentSelectiveIntegration class
├── tests/
│   └── test_core.py       # 3 passing tests
├── docs/
│   └── index.md
└── requirements.txt
```

## Getting Started

```bash
cd adsi
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

## Three Convergent Patterns

1. **Integration-Validation Architecture** — both systems use activity-dependent selection as an isomorphic process (gradient-backpropagation ↔ Hebbian-plasticity)
2. **Learning Rate ↔ Trophic Factor** — both use a plasticity control parameter with inverted-U dose-response (BDNF follows the same curve as learning rate schedules)
3. **Capacity-Learning Tradeoff** — both evolved homeostatic mechanisms to solve the stability-plasticity dilemma

## API

### `ActivityDependentSelectiveIntegration(learning_rate, pruning_threshold)`

Simulates the integration-validation pipeline:
- `learning_rate`: Controls plasticity strength (0.0–1.0). Maps to BDNF trophic factor analogy.
- `pruning_threshold`: Minimum contribution score for survival (0.0–1.0)

### `engine.integrate(new_elements, existing_system)`

Returns a result dict with: `specified`, `initialized`, `survived`, `pruned`, `system_updated`.

### `learning_rate_to_bdnf(learning_rate)`

Returns a human-readable string mapping learning rate to biological BDNF dose-response.

## Origin

This project was scaffolded by SDEAS Phase 15 — Epistemic Embodiment.
Source: Creative cycle `CYC-D0E35B87` | Publication: `PUB-1D30463A`
Approved: 2026-05-12

## License

MIT
