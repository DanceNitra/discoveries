"""Tests for swarm_orchestrator_and_multi_agent_team.core"""
import pytest
from swarm_orchestrator_and_multi_agent_team.core import ActivityDependentSelectiveIntegration

def test_integration_basic():
    engine = ActivityDependentSelectiveIntegration(learning_rate=0.01, pruning_threshold=0.3)
    elements = [
        {"id": "strong", "signal_strength": 0.9, "novelty": 0.5},
        {"id": "weak", "signal_strength": 0.1, "novelty": 0.2},
    ]
    result = engine.integrate(elements, {})
    assert result["specified"] == 2
    assert result["survived"] == 1
    assert result["pruned"] == 1
    assert "strong" in result["system_updated"]

def test_all_pruned():
    engine = ActivityDependentSelectiveIntegration(learning_rate=0.01, pruning_threshold=0.9)
    result = engine.integrate([{"id": "x", "signal_strength": 0.1, "novelty": 0.1}], {})
    assert result["pruned"] == 1
    assert result["survived"] == 0
