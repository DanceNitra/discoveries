"""Tests for homeostasis_agent_regulation.main"""
import pytest
from homeostasis_agent_regulation.main import (
    HomeostaticLoop,
    HomeostaticAgent,
    LoopConfig,
    LoopState,
    create_default_agent,
    __version__,
)


class TestHomeostaticLoop:

    def test_loop_step_produces_state(self):
        config = LoopConfig(
            set_points={"temperature": 37.0},
            tolerances={"temperature": 0.5},
            effector_bounds={"temperature": (-1.0, 1.0)},
        )
        loop = HomeostaticLoop(config)
        state = loop.step()
        assert isinstance(state, LoopState)
        assert "temperature" in state.errors
        assert state.loop_count == 1

    def test_effector_bounds_clamp_output(self):
        config = LoopConfig(
            set_points={"x": 0.0},
            tolerances={"x": 0.1},
            effector_bounds={"x": (-0.1, 0.1)},
        )
        loop = HomeostaticLoop(config)
        state = loop.step()
        # With default sensor returning 0, error = 0, correction = 0
        assert state.effector_outputs["x"] == 0.0

    def test_allostatic_load_tracks_error(self):
        config = LoopConfig(
            set_points={"val": 100.0},
            tolerances={"val": 1.0},
            effector_bounds={"val": (-10.0, 10.0)},
        )
        loop = HomeostaticLoop(config)
        for _ in range(5):
            loop.step()
        assert loop.state.allostatic_load.error_samples == 5
        assert loop.state.allostatic_load.cumulative_error > 0

    def test_set_point_drift_under_chronic_error(self):
        """Chronic high error should cause set points to drift."""
        config = LoopConfig(
            set_points={"val": 100.0},
            tolerances={"val": 1.0},
            effector_bounds={"val": (-50.0, 50.0)},
            drift_rate=0.1,
        )
        loop = HomeostaticLoop(config)
        original_sp = loop.set_points["val"]
        # Override sensor to always report 0 (big error)
        loop.sensor_fn = lambda: {"val": 0.0}
        for _ in range(10):
            loop.step()
        self.assert_drifted(loop.set_points["val"], original_sp)

    def assert_drifted(self, current, original):
        """Helper: assert the value has drifted by a meaningful amount."""
        assert abs(current - original) > 0.001, (
            f"Expected set point to drift from {original}, got {current}"
        )

    def test_positive_feedback_detection(self):
        config = LoopConfig(
            set_points={"a": 0.0},
            tolerances={"a": 0.1},
            effector_bounds={"a": (-1.0, 1.0)},
        )
        loop = HomeostaticLoop(config)
        # Override effector to return same-sign as error (positive feedback)
        loop.effector_fn = lambda corr: {"a": corr["a"]}
        # Override sensor to always report a negative error with positive correction
        loop.sensor_fn = lambda: {"a": 5.0}  # error = -5 (set_point 0 - 5 = -5)
        # Make pid produce positive correction? Actually with set_point 0 and sensed 5,
        # error = -5, correction = -2.5. For positive feedback, we need same sign.
        # Override effector to flip sign
        loop.effector_fn = lambda corr: {"a": abs(corr["a"]) if corr["a"] < 0 else -corr["a"]}
        # Actually simpler: set sensor so error is positive, effector outputs positive
        # set_point 0, sensor -5 → error = 5, correction = 2.5
        loop.sensor_fn = lambda: {"a": -5.0}
        loop.effector_fn = lambda corr: {"a": 3.0}  # same sign as correction (positive)
        # But the detection checks error vs correction signs. error=5, correction=2.5
        # Both positive → positive feedback detected
        for _ in range(3):
            loop.step()
        assert loop.state.positive_feedback_detected, \
            "Expected positive feedback to be detected"

    def test_reset_loop(self):
        config = LoopConfig(
            set_points={"x": 10.0},
            tolerances={"x": 1.0},
            effector_bounds={"x": (-5.0, 5.0)},
        )
        loop = HomeostaticLoop(config)
        loop.sensor_fn = lambda: {"x": 0.0}
        loop.step()
        loop.step()
        assert loop.state.loop_count == 2
        loop.reset()
        assert loop.state.loop_count == 0
        assert loop.state.allostatic_load.cumulative_error == 0.0
        assert not loop.state.positive_feedback_detected


class TestHomeostaticAgent:

    def test_agent_step_runs_turn_loops_only(self):
        agent = create_default_agent("test_agent")
        results = agent.step()
        # Only per-turn loops run on step()
        assert "per_turn" in results
        assert agent.turn_count == 1

    def test_agent_end_session_runs_session_loops(self):
        agent = create_default_agent("test_agent")
        agent.step()
        agent.step()
        results = agent.end_session()
        assert "per_session" in results
        assert agent.session_count == 1

    def test_cross_session_update_runs_cross_loops(self):
        agent = create_default_agent("test_agent")
        results = agent.cross_session_update()
        assert "cross_session" in results

    def test_nested_timescales_together(self):
        """All three timescales operate concurrently without interference."""
        agent = create_default_agent("nested")
        # Simulate a full lifecycle
        for _ in range(3):
            agent.step()
        agent.end_session()
        agent.cross_session_update()
        report = agent.get_allostatic_load_report()
        assert "per_turn" in report
        assert "per_session" in report
        assert "cross_session" in report

    def test_allostatic_load_report(self):
        agent = create_default_agent("load_test")
        for _ in range(5):
            agent.step()
        agent.end_session()
        report = agent.get_allostatic_load_report()
        assert report["per_turn"].error_samples > 0
        assert report["per_turn"].cumulative_error > 0

    def test_positive_feedback_escape_report(self):
        agent = create_default_agent("fb_test")
        agent.step()
        escape = agent.has_positive_feedback_escape()
        assert isinstance(escape, dict)
        assert "per_turn" in escape

    def test_set_points_report(self):
        agent = create_default_agent("sp_test")
        sp = agent.get_set_points()
        assert "per_turn" in sp
        assert "motor_error" in sp["per_turn"]
        assert sp["per_turn"]["motor_error"] == 0.0

    def test_agent_reset(self):
        agent = create_default_agent("reset_test")
        agent.step()
        agent.end_session()
        agent.reset()
        assert agent.turn_count == 0
        assert agent.session_count == 0
        assert len(agent._history) == 0

    def test_multiple_steps_increase_load(self):
        agent = create_default_agent("multi")
        for _ in range(10):
            agent.step()
        report = agent.get_allostatic_load_report()
        # More steps should produce higher cumulative error
        load_after_10 = report["per_turn"].cumulative_error
        for _ in range(10):
            agent.step()
        report = agent.get_allostatic_load_report()
        load_after_20 = report["per_turn"].cumulative_error
        assert load_after_20 > load_after_10, (
            "Cumulative error should increase with more steps"
        )

    def test_drift_under_sustained_error(self):
        """Sustained error causes set point drift (allostatic load)."""
        agent = create_default_agent("drift_test")
        turn_loop = agent._loops["per_turn"]
        # Force sustained error
        turn_loop.sensor_fn = lambda: {"motor_error": 5.0, "activation": 0.0}
        original_motor = agent.get_set_points()["per_turn"]["motor_error"]
        for _ in range(20):
            agent.step()
        drifted_motor = agent.get_set_points()["per_turn"]["motor_error"]
        assert drifted_motor != original_motor, (
            "Set point should drift under sustained error"
        )

    def test_version(self):
        assert __version__ == "0.1.0"
