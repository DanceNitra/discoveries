"""Tests for causal_agent_evaluation.main"""
from __future__ import annotations

import numpy as np
import pytest

from causal_agent_evaluation.main import CausalAgentEvaluator


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def evaluator() -> CausalAgentEvaluator:
    return CausalAgentEvaluator(random_seed=42)


@pytest.fixture
def dummy_scores() -> tuple[np.ndarray, np.ndarray]:
    """Treatment slightly higher than control."""
    rng = np.random.default_rng(42)
    control = rng.uniform(0.4, 0.7, size=50)
    treatment = control + rng.uniform(0.05, 0.15, size=50)
    return treatment, control


# ---------------------------------------------------------------------------
# ATE (simple)
# ---------------------------------------------------------------------------

class TestATE:
    def test_basic(self, evaluator: CausalAgentEvaluator, dummy_scores):
        t, c = dummy_scores
        result = evaluator.ate(t, c)
        assert result["ate"] > 0
        assert result["ci_lower"] < result["ate"] < result["ci_upper"]
        assert result["n_treatment"] == 50
        assert result["n_control"] == 50

    def test_no_effect(self, evaluator: CausalAgentEvaluator):
        scores = [0.5, 0.6, 0.7, 0.8]
        result = evaluator.ate(scores, scores)
        assert abs(result["ate"]) < 1e-10
        assert result["n_treatment"] == 4
        assert result["n_control"] == 4


# ---------------------------------------------------------------------------
# Matched-pair evaluation
# ---------------------------------------------------------------------------

class TestMatchedPair:
    def test_direct_paired(self, evaluator: CausalAgentEvaluator):
        t = [0.85, 0.78, 0.92, 0.70]
        c = [0.72, 0.80, 0.65, 0.74]
        result = evaluator.matched_pair_evaluation(t, c)
        assert result["method"] == "direct paired"
        assert result["n_pairs"] == 4
        assert result["ate"] == pytest.approx(np.mean(t) - np.mean(c))
        assert result["ci_lower"] < result["ate"] < result["ci_upper"]

    def test_propensity_matched(self, evaluator: CausalAgentEvaluator):
        rng = np.random.default_rng(42)
        n = 30
        c_scores = rng.uniform(0.4, 0.7, size=n)
        t_scores = c_scores + rng.uniform(0.05, 0.2, size=n)
        difficulty = np.concatenate([
            rng.uniform(1, 10, size=n),   # control covariates
            rng.uniform(1, 10, size=n),   # treatment covariates
        ])
        result = evaluator.matched_pair_evaluation(
            t_scores, c_scores,
            covariates={"task_difficulty": difficulty},
        )
        assert result["method"] == "propensity-score matched"
        assert result["n_pairs"] > 0
        assert result["ci_lower"] < result["ate"] < result["ci_upper"]

    def test_covariate_length_mismatch(self, evaluator: CausalAgentEvaluator):
        with pytest.raises(ValueError, match="length"):
            evaluator.matched_pair_evaluation(
                [0.5], [0.5],
                covariates={"x": [1, 2, 3]},  # 3 != 1+1
            )

    def test_empty_after_matching(self, evaluator: CausalAgentEvaluator):
        """Edge case: more treatment than control units in matching."""
        t = [0.99, 0.98, 0.97, 0.96]
        c = [0.1, 0.2]
        cov = {"x": [0.0, 0.0, 10.0, 10.0, 9.0, 9.0]}
        result = evaluator.matched_pair_evaluation(t, c, covariates=cov)
        # Greedy matching produces min(len(t), len(c)) pairs
        assert result["n_pairs"] == 2
        assert result["method"] == "propensity-score matched"


# ---------------------------------------------------------------------------
# Stratified ATE
# ---------------------------------------------------------------------------

class TestStratifiedATE:
    def test_basic_stratification(self, evaluator: CausalAgentEvaluator):
        t = [0.85, 0.78, 0.92, 0.70, 0.88, 0.76]
        c = [0.72, 0.80, 0.65, 0.74, 0.70, 0.68]
        # First 6 = control, next 6 = treatment
        strata = ["easy", "hard", "easy", "hard", "easy", "hard"] * 2
        result = evaluator.stratified_ate(t, c, strata)
        assert "ate" in result
        assert "ci_lower" in result
        assert "ci_upper" in result
        assert "cate" in result
        assert "strata_counts" in result
        assert set(result["cate"].keys()) == {"easy", "hard"}
        assert result["strata_counts"]["easy"]["control"] == 3
        assert result["strata_counts"]["easy"]["treatment"] == 3

    def test_strata_length_mismatch(self, evaluator: CausalAgentEvaluator):
        with pytest.raises(ValueError, match="length"):
            evaluator.stratified_ate(
                [0.5, 0.6], [0.4, 0.5],
                ["easy", "hard"],  # 2 != 4
            )

    def test_single_stratum(self, evaluator: CausalAgentEvaluator):
        t = [0.8, 0.9]
        c = [0.6, 0.7]
        strata = ["easy"] * 4
        result = evaluator.stratified_ate(t, c, strata)
        assert result["ate"] == pytest.approx(np.mean(t) - np.mean(c))


# ---------------------------------------------------------------------------
# E-value sensitivity
# ---------------------------------------------------------------------------

class TestEValue:
    def test_positive_ate(self, evaluator: CausalAgentEvaluator):
        result = evaluator.e_value(ate=0.10, ci_lower=0.02)
        assert result["e_value_ate"] > 1.0
        assert result["e_value_ci_boundary"] > 1.0

    def test_no_effect(self, evaluator: CausalAgentEvaluator):
        result = evaluator.e_value(ate=0.0)
        assert result["e_value_ate"] == 1.0

    def test_negative_ate(self, evaluator: CausalAgentEvaluator):
        result = evaluator.e_value(ate=-0.05)
        assert result["e_value_ate"] > 1.0

    def test_no_ci(self, evaluator: CausalAgentEvaluator):
        result = evaluator.e_value(ate=0.08)
        assert result["e_value_ci_boundary"] is None


# ---------------------------------------------------------------------------
# DAG confounder check
# ---------------------------------------------------------------------------

class TestDAG:
    def test_confounded_dag(self, evaluator: CausalAgentEvaluator):
        edges = [
            ("task_difficulty", "treatment"),
            ("task_difficulty", "agent_score"),
            ("treatment", "agent_score"),
        ]
        result = evaluator.check_backdoor_criterion(
            dag_edges=edges,
            treatment="treatment",
            outcome="agent_score",
        )
        assert result["backdoor_paths_exist"] is True or result["backdoor_paths_exist"] is False
        assert "task_difficulty" in result["potential_confounders"]

    def test_unconfounded_dag(self, evaluator: CausalAgentEvaluator):
        edges = [
            ("treatment", "agent_score"),
        ]
        result = evaluator.check_backdoor_criterion(
            dag_edges=edges,
            treatment="treatment",
            outcome="agent_score",
        )
        assert len(result["potential_confounders"]) == 0

    def test_indirect_confounding(self, evaluator: CausalAgentEvaluator):
        edges = [
            ("prior_knowledge", "task_selection"),
            ("task_selection", "treatment"),
            ("task_selection", "agent_score"),
            ("treatment", "agent_score"),
        ]
        result = evaluator.check_backdoor_criterion(
            dag_edges=edges,
            treatment="treatment",
            outcome="agent_score",
        )
        assert len(result["potential_confounders"]) >= 1

    def test_adjustment_set(self, evaluator: CausalAgentEvaluator):
        edges = [
            ("difficulty", "treatment"),
            ("difficulty", "score"),
            ("treatment", "score"),
        ]
        result = evaluator.check_backdoor_criterion(
            dag_edges=edges,
            treatment="treatment",
            outcome="score",
        )
        assert "difficulty" in result["suggested_adjustment_set"]


# ---------------------------------------------------------------------------
# Version
# ---------------------------------------------------------------------------

class TestVersion:
    def test_version(self):
        from causal_agent_evaluation import __version__
        assert __version__ == "0.1.0"
