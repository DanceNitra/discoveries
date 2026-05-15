"""
causal_agent_evaluation.main -- Core implementation

Causal Inference for AI Agent Evaluation:
  - Matched-pair evaluation (propensity score matching)
  - Stratification by task difficulty (blocking)
  - ATE estimation with bootstrap confidence intervals
  - E-value sensitivity analysis
  - DAG-based confounder check (backdoor criterion)
"""

from __future__ import annotations

import math
import random
from collections import Counter
from typing import Any, Optional

import numpy as np
from numpy.typing import ArrayLike

__version__ = "0.1.0"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _logit(p: np.ndarray) -> np.ndarray:
    """Logit function, clipped to avoid infinities (vectorized)."""
    p = np.clip(p, 1e-12, 1 - 1e-12)
    return np.log(p / (1.0 - p))


def _expit(x: np.ndarray) -> np.ndarray:
    """Logistic sigmoid (vectorized)."""
    return np.where(
        x < -700, 0.0,
        np.where(x > 700, 1.0, 1.0 / (1.0 + np.exp(-x)))
    )


def _bootstrap_ci(
    treatment: np.ndarray,
    control: np.ndarray,
    n_bootstrap: int = 2000,
    ci: float = 0.95,
    random_seed: Optional[int] = None,
) -> tuple[float, float, float]:
    """Bootstrap ATE and percentile confidence interval."""
    rng = np.random.default_rng(random_seed)
    n_t = len(treatment)
    n_c = len(control)
    estimates: list[float] = []
    for _ in range(n_bootstrap):
        tb = rng.choice(treatment, size=n_t, replace=True)
        cb = rng.choice(control, size=n_c, replace=True)
        estimates.append(float(np.mean(tb) - np.mean(cb)))
    estimates = np.array(estimates)
    alpha = 1.0 - ci
    lo, hi = np.percentile(estimates, [alpha / 2 * 100, (1 - alpha / 2) * 100])
    ate = float(np.mean(treatment) - np.mean(control))
    return ate, float(lo), float(hi)


# ---------------------------------------------------------------------------
# Main evaluator
# ---------------------------------------------------------------------------

class CausalAgentEvaluator:
    """Causal inference toolkit for AI agent evaluation.

    Implements the Potential Outcomes Framework adapted to the problem of
    evaluating changes to AI agent systems.
    """

    def __init__(self, random_seed: Optional[int] = None) -> None:
        self._rng = random.Random(random_seed)
        self._np_rng = np.random.default_rng(random_seed)
        self._random_seed = random_seed

    # ---- Matched-pair evaluation ---------------------------------------

    def matched_pair_evaluation(
        self,
        treatment_scores: ArrayLike,
        control_scores: ArrayLike,
        covariates: Optional[dict[str, ArrayLike]] = None,
        n_bootstrap: int = 2000,
        ci: float = 0.95,
    ) -> dict[str, Any]:
        """Matched-pair A/B evaluation with optional propensity-score matching.

        When *covariates* are supplied, pairs are built by nearest-neighbour
        matching on the estimated propensity score (logistic regression on
        task-difficulty-like covariates). Otherwise direct one-to-one pairing
        (truncated to min length) is used.

        Parameters
        ----------
        treatment_scores : array-like
            Scores from the treatment (new) agent configuration.
        control_scores : array-like
            Scores from the control (baseline) agent configuration.
        covariates : dict[str, array-like], optional
            Covariates for propensity-score matching. Each key is a covariate
            name and the value an array of length equal to the combined sample.
            The first half is assumed to correspond to control, the second to
            treatment (matching the order of *control_scores* then
            *treatment_scores*).
        n_bootstrap : int
            Bootstrap iterations for confidence interval.
        ci : float
            Confidence level (default 0.95).

        Returns
        -------
        dict with keys: ate, ci_lower, ci_upper, n_pairs, matched_pairs, method
        """
        t_arr = np.asarray(treatment_scores, dtype=float).ravel()
        c_arr = np.asarray(control_scores, dtype=float).ravel()

        if covariates is not None:
            # Build design matrix for propensity-score model
            names = sorted(covariates.keys())
            X_list: list[np.ndarray] = []
            for name in names:
                col = np.asarray(covariates[name], dtype=float).ravel()
                if len(col) != len(t_arr) + len(c_arr):
                    raise ValueError(
                        f"Covariate '{name}' length {len(col)} != total "
                        f"samples {len(t_arr) + len(c_arr)}"
                    )
                X_list.append(col)
            X = np.column_stack(X_list)
            # Propensity model: logistic regression via Newton-Raphson
            coefs = self._logistic_regression(X)
            # Augment X with intercept for prediction
            X_aug = np.column_stack([np.ones(len(X)), X])
            pscores = _expit(X_aug @ coefs)
            # Split: first half = control indices, second half = treatment
            n_c = len(c_arr)
            ps_t = pscores[n_c:]   # treatment propensity scores
            ps_c = pscores[:n_c]   # control propensity scores
            # Greedy nearest-neighbour matching on logit propensity
            logit_t = np.array([_logit(p) for p in ps_t])
            logit_c = np.array([_logit(p) for p in ps_c])
            matched_t: list[int] = []
            matched_c: list[int] = []
            used_c: set[int] = set()
            for i in range(len(logit_t)):
                dists = np.abs(logit_c - logit_t[i])
                # Exclude already used
                for u in sorted(used_c):
                    dists[u] = np.inf
                j = int(np.argmin(dists))
                if dists[j] < np.inf:
                    matched_t.append(i)
                    matched_c.append(j)
                    used_c.add(j)
            n_pairs = len(matched_t)
            if n_pairs == 0:
                raise ValueError("No valid matched pairs could be formed.")
            t_matched = t_arr[matched_t]
            c_matched = c_arr[matched_c]
            method = "propensity-score matched"
        else:
            # Direct pairing: truncate to shorter length
            n_pairs = min(len(t_arr), len(c_arr))
            t_matched = t_arr[:n_pairs]
            c_matched = c_arr[:n_pairs]
            method = "direct paired"

        ate, lo, hi = _bootstrap_ci(
            t_matched,
            c_matched,
            n_bootstrap=n_bootstrap,
            ci=ci,
            random_seed=self._random_seed,
        )

        return {
            "ate": ate,
            "ci_lower": lo,
            "ci_upper": hi,
            "n_pairs": n_pairs,
            "method": method,
        }

    # ---- Stratified ATE -------------------------------------------------

    def stratified_ate(
        self,
        treatment_scores: ArrayLike,
        control_scores: ArrayLike,
        strata_labels: ArrayLike,
        n_bootstrap: int = 2000,
        ci: float = 0.95,
    ) -> dict[str, Any]:
        """Stratified ATE by task difficulty or other blocking variable.

        Returns both overall ATE (weighted by stratum size) and per-stratum
        conditional ATE (CATE).

        Parameters
        ----------
        treatment_scores : array-like
            Scores for the treatment group.
        control_scores : array-like
            Scores for the control group.
        strata_labels : array-like
            Stratum label per observation. Length must equal sum of lengths
            of treatment_scores and control_scores (first half = control,
            second half = treatment).
        n_bootstrap : int
            Bootstrap iterations.
        ci : float
            Confidence level.

        Returns
        -------
        dict with keys: ate, ci_lower, ci_upper, cate (dict), strata_counts
        """
        t_arr = np.asarray(treatment_scores, dtype=float).ravel()
        c_arr = np.asarray(control_scores, dtype=float).ravel()
        labels = np.asarray(strata_labels)
        total = len(t_arr) + len(c_arr)
        if len(labels) != total:
            raise ValueError(
                f"strata_labels length {len(labels)} != total samples {total}"
            )

        n_c = len(c_arr)
        labels_c = labels[:n_c]
        labels_t = labels[n_c:]

        strata_names = sorted(set(str(l) for l in labels))
        cate: dict[str, float] = {}
        counts: dict[str, dict[str, int]] = {}
        weighted_sum = 0.0
        total_weight = 0

        for s in strata_names:
            mask_c = np.array([str(l) == s for l in labels_c])
            mask_t = np.array([str(l) == s for l in labels_t])
            c_s = c_arr[mask_c]
            t_s = t_arr[mask_t]
            n_cs = len(c_s)
            n_ts = len(t_s)
            counts[s] = {"control": int(n_cs), "treatment": int(n_ts)}
            if n_cs > 0 and n_ts > 0:
                ate_s = float(np.mean(t_s) - np.mean(c_s))
            else:
                ate_s = 0.0
            cate[s] = ate_s
            weight = n_cs + n_ts
            weighted_sum += ate_s * weight
            total_weight += weight

        overall_ate = weighted_sum / total_weight if total_weight > 0 else 0.0

        # Bootstrap CI on overall weighted ATE
        rng = np.random.default_rng(self._random_seed)
        boot_ates: list[float] = []
        for _ in range(n_bootstrap):
            ws = 0.0
            tw = 0
            for s in strata_names:
                mask_c = np.array([str(l) == s for l in labels_c])
                mask_t = np.array([str(l) == s for l in labels_t])
                c_s = c_arr[mask_c]
                t_s = t_arr[mask_t]
                if len(c_s) == 0 or len(t_s) == 0:
                    continue
                tb = rng.choice(t_s, size=len(t_s), replace=True)
                cb = rng.choice(c_s, size=len(c_s), replace=True)
                ate_b = float(np.mean(tb) - np.mean(cb))
                w = len(c_s) + len(t_s)
                ws += ate_b * w
                tw += w
            boot_ates.append(ws / tw if tw > 0 else 0.0)

        boot_ates = np.array(boot_ates)
        alpha = 1.0 - ci
        lo, hi = np.percentile(boot_ates, [alpha / 2 * 100, (1 - alpha / 2) * 100])

        return {
            "ate": overall_ate,
            "ci_lower": float(lo),
            "ci_upper": float(hi),
            "cate": cate,
            "strata_counts": counts,
        }

    # ---- ATE (simple) ---------------------------------------------------

    def ate(
        self,
        treatment_scores: ArrayLike,
        control_scores: ArrayLike,
        n_bootstrap: int = 2000,
        ci: float = 0.95,
    ) -> dict[str, Any]:
        """Simple ATE with bootstrap CI (no covariate adjustment).

        Parameters
        ----------
        treatment_scores : array-like
        control_scores : array-like
        n_bootstrap : int
        ci : float

        Returns
        -------
        dict with keys: ate, ci_lower, ci_upper, n_treatment, n_control
        """
        t_arr = np.asarray(treatment_scores, dtype=float).ravel()
        c_arr = np.asarray(control_scores, dtype=float).ravel()
        ate_val, lo, hi = _bootstrap_ci(
            t_arr,
            c_arr,
            n_bootstrap=n_bootstrap,
            ci=ci,
            random_seed=self._random_seed,
        )
        return {
            "ate": ate_val,
            "ci_lower": lo,
            "ci_upper": hi,
            "n_treatment": int(len(t_arr)),
            "n_control": int(len(c_arr)),
        }

    # ---- E-value sensitivity --------------------------------------------

    def e_value(
        self,
        ate: float,
        ci_lower: Optional[float] = None,
    ) -> dict[str, Any]:
        """E-value sensitivity analysis (VanderWeele & Ding, 2017).

        The E-value is the minimum strength of association (on the risk-ratio
        scale) that an unmeasured confounder would need to have with *both*
        the treatment and the outcome to explain away the observed ATE.

        Parameters
        ----------
        ate : float
            Observed average treatment effect (can be negative; absolute
            value is used for the computation).
        ci_lower : float, optional
            Lower bound of the 95% confidence interval for the ATE.
            If provided, computes the E-value for the CI boundary as well.

        Returns
        -------
        dict with keys: e_value_ate, e_value_ci_boundary
        """
        # Convert ATE on difference scale to approximate risk ratio
        # We assume the outcome is bounded [0,1] (e.g., normalized scores).
        # For difference d, the minimum risk ratio compatible with d
        # is given by VanderWeele & Ding formula.
        def _e_val(d: float) -> float:
            if d <= 0:
                return 1.0  # no confounding needed
            rr = 1.0 + abs(d)  # conservative approximation
            # VanderWeele & Ding: E = RR + sqrt(RR * (RR - 1))
            # when we map difference d -> risk ratio 1 + |d|
            # For a more conservative / standard formula:
            # E = 1 + sqrt(1 + 2*|d|) ... but we use the published formula:
            # E_val = (1 + sqrt(1 + 2*|d|)) / 2 ... no, the proper formula:
            # If observed RR = exp(beta), then E = RR + sqrt(RR*(RR-1)).
            # We set RR = 1 + |d| as a conservative mapping.
            if rr <= 1.0:
                return 1.0
            return rr + math.sqrt(rr * (rr - 1.0))

        e_ate = _e_val(abs(ate))
        e_ci = _e_val(abs(ci_lower)) if ci_lower is not None else 1.0

        return {
            "e_value_ate": round(e_ate, 4),
            "e_value_ci_boundary": round(e_ci, 4) if ci_lower is not None else None,
        }

    # ---- DAG confounder check -------------------------------------------

    def check_backdoor_criterion(
        self,
        dag_edges: list[tuple[str, str]],
        treatment: str,
        outcome: str,
    ) -> dict[str, Any]:
        """Check the backdoor criterion for a given DAG.

        This implements a simple graphical check: are there any unblocked
        backdoor paths from treatment to outcome? Uses a reachability-based
        test: nodes that are ancestors of both treatment and outcome are
        potential confounders.

        Parameters
        ----------
        dag_edges : list of (str, str)
            Directed edges as (parent, child) tuples.
        treatment : str
            Name of the treatment node.
        outcome : str
            Name of the outcome node.

        Returns
        -------
        dict with keys:
          - backdoor_paths_exist (bool)
          - potential_confounders (list)
          - suggested_adjustment_set (list)
          - parents_of_treatment (list)
        """
        # Build adjacency
        children: dict[str, list[str]] = {}
        parents: dict[str, list[str]] = {}
        all_nodes: set[str] = set()
        for p, c in dag_edges:
            all_nodes.add(p)
            all_nodes.add(c)
            children.setdefault(p, []).append(c)
            parents.setdefault(c, []).append(p)

        # Find ancestors of a node (recursive)
        def _ancestors(node: str, _seen: set[str] | None = None) -> set[str]:
            if _seen is None:
                _seen = set()
            _seen.add(node)
            for par in parents.get(node, []):
                if par not in _seen:
                    _ancestors(par, _seen)
            return _seen

        anc_t = _ancestors(treatment)
        anc_o = _ancestors(outcome)

        # Potential confounders: common ancestors (excluding treatment itself)
        potential_conf = sorted(
            (anc_t & anc_o) - {treatment}
        )

        # Check for backdoor paths: any path from treatment to outcome that
        # starts with an edge into treatment
        # Simple check: does any parent of treatment have a directed path to outcome
        # (excluding the edge through treatment)?
        backdoor_paths = False
        for p in parents.get(treatment, []):
            # Can we reach outcome from p without going through treatment?
            # We do BFS on the subgraph excluding edges from/to treatment
            reachable: set[str] = set()
            stack: list[str] = [p]
            while stack:
                node = stack.pop()
                if node == outcome:
                    backdoor_paths = True
                    break
                if node in reachable:
                    continue
                reachable.add(node)
                for ch in children.get(node, []):
                    if ch != treatment and ch not in reachable:
                        stack.append(ch)
            if backdoor_paths:
                break

        # Suggested adjustment set: for the simple DAG this is just the
        # parents of treatment that are not descendants of outcome
        # (backdoor criterion)
        adjustment = sorted(
            set(parents.get(treatment, [])) & anc_o
        )
        if not adjustment:
            # Minimal: use potential confounders
            adjustment = potential_conf

        return {
            "backdoor_paths_exist": backdoor_paths,
            "potential_confounders": potential_conf,
            "suggested_adjustment_set": adjustment,
            "parents_of_treatment": sorted(parents.get(treatment, [])),
        }

    # ---- Internal: logistic regression ----------------------------------

    def _logistic_regression(
        self,
        X: np.ndarray,
        max_iter: int = 100,
        tol: float = 1e-8,
    ) -> np.ndarray:
        """Newton-Raphson logistic regression.

        Returns coefficient vector (intercept appended to X).
        """
        n, p = X.shape
        # Add intercept
        X_aug = np.column_stack([np.ones(n), X])
        # Response: 0 for first half (control), 1 for second half (treatment)
        half = n // 2
        y = np.zeros(n)
        y[half:] = 1.0

        beta = np.zeros(p + 1)
        for _ in range(max_iter):
            eta = X_aug @ beta
            pi_ = _expit(eta)
            grad = X_aug.T @ (y - pi_)
            W_diag = pi_ * (1.0 - pi_)
            hess = -X_aug.T @ (X_aug * W_diag[:, np.newaxis])
            try:
                delta = np.linalg.solve(hess, grad)
            except np.linalg.LinAlgError:
                delta = grad * 0.01
            beta -= delta
            if np.linalg.norm(delta) < tol:
                break
        return beta
