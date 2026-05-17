"""
homeostasis_agent_regulation.main -- Core implementation

Implements the four-component homeostatic negative-feedback loop as a model
for agent self-regulation:

  Sensor → Comparator → Effector → Feedback path

With support for:
  - Nested loops at per-turn, per-session, and cross-session timescales
  - Allostatic load tracking (set point drift under chronic error)
  - Positive feedback escape detection and bounded effector protection
"""

__version__ = "0.1.0"

import math
import time
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

SensorReading = float
ErrorMetric = float
SetPoint = float

SensorFn = Callable[[], Dict[str, SensorReading]]
EffectorFn = Callable[[Dict[str, float]], Dict[str, float]]
FeedbackFn = Callable[[Dict[str, float]], Dict[str, SensorReading]]


# ---------------------------------------------------------------------------
# Core data structures
# ---------------------------------------------------------------------------

@dataclass
class AllostaticLoadRecord:
    """Tracks chronic error accumulation and set point drift over time."""
    cumulative_error: float = 0.0
    drift_per_channel: Dict[str, float] = field(default_factory=dict)
    peak_error: float = 0.0
    error_samples: int = 0


@dataclass
class LoopConfig:
    """Configuration for a single homeostatic loop."""
    set_points: Dict[str, float]
    tolerances: Dict[str, float]
    effector_bounds: Dict[str, Tuple[float, float]]  # channel → (min, max)
    drift_rate: float = 0.01        # how fast set points drift under load
    recovery_rate: float = 0.005    # how fast set points recover when error is low
    name: str = "default"


@dataclass
class LoopState:
    """Runtime state of a single homeostatic loop."""
    errors: Dict[str, float] = field(default_factory=dict)
    effector_outputs: Dict[str, float] = field(default_factory=dict)
    allostatic_load: AllostaticLoadRecord = field(default_factory=AllostaticLoadRecord)
    positive_feedback_detected: bool = False
    loop_count: int = 0


# ---------------------------------------------------------------------------
# HomeostaticLoop — single self-regulation loop
# ---------------------------------------------------------------------------

class HomeostaticLoop:
    """
    A single four-component negative-feedback homeostatic loop.

    Components:
      1. Sensor   — reads current state metrics via sensor_fn
      2. Comparator — computes error = set_point - sensed_value
      3. Effector  — applies corrective actions via effector_fn
      4. Feedback  — observes post-action state via feedback_fn
    """

    def __init__(
        self,
        config: LoopConfig,
        sensor_fn: Optional[SensorFn] = None,
        effector_fn: Optional[EffectorFn] = None,
        feedback_fn: Optional[FeedbackFn] = None,
    ):
        self.config = config
        self.sensor_fn = sensor_fn or self._default_sensor
        self.effector_fn = effector_fn or self._default_effector
        self.feedback_fn = feedback_fn or self._default_feedback
        self.state = LoopState()
        self._set_points = dict(config.set_points)

    # -- Default passthrough stubs (override with real functions) -----------

    def _default_sensor(self) -> Dict[str, SensorReading]:
        return {ch: 0.0 for ch in self.config.set_points}

    def _default_effector(self, corrections: Dict[str, float]) -> Dict[str, float]:
        return corrections

    def _default_feedback(self, outputs: Dict[str, float]) -> Dict[str, SensorReading]:
        return {k: v for k, v in outputs.items()}

    # -- Core loop execution ------------------------------------------------

    def step(self) -> LoopState:
        """Execute one iteration of the homeostatic loop."""
        # 1. SENSE
        readings = self.sensor_fn()

        # 2. COMPARE
        errors = {}
        for channel, set_point in self._set_points.items():
            sensed = readings.get(channel, 0.0)
            errors[channel] = set_point - sensed

        # Track allostatic load
        for ch, err in errors.items():
            self.state.allostatic_load.cumulative_error += abs(err)
            if abs(err) > self.state.allostatic_load.peak_error:
                self.state.allostatic_load.peak_error = abs(err)
        self.state.allostatic_load.error_samples += 1

        # Update per-channel drift
        for ch, err in errors.items():
            prev = self.state.allostatic_load.drift_per_channel.get(ch, 0.0)
            self.state.allostatic_load.drift_per_channel[ch] = prev + abs(err)

        # 3. EFFECTOR — compute corrections with bounds
        corrections = {}
        for channel, err in errors.items():
            raw_correction = self._pid_correction(channel, err)
            lo, hi = self.config.effector_bounds.get(channel, (-1.0, 1.0))
            corrections[channel] = max(lo, min(hi, raw_correction))

        # Check for positive feedback (correction amplifies error instead of damping)
        self._detect_positive_feedback(errors, corrections)

        outputs = self.effector_fn(corrections)
        self.state.effector_outputs = outputs
        self.state.errors = errors
        self.state.loop_count += 1

        # 4. FEEDBACK (optional, used by outer loops)
        self.feedback_fn(outputs)

        # Allostatic drift: shift set points under chronic load
        self._update_set_points()

        return self.state

    def _pid_correction(self, channel: str, error: float) -> float:
        """Simple proportional correction with a damping factor."""
        kp = 0.5  # proportional gain
        return kp * error

    def _detect_positive_feedback(
        self, errors: Dict[str, float], corrections: Dict[str, float]
    ) -> None:
        """
        Detect positive feedback escape: when a correction has the same sign
        as the error it's supposed to reduce (correction amplifies error).
        """
        positive_count = 0
        for ch in errors:
            if errors[ch] != 0.0 and corrections.get(ch, 0.0) != 0.0:
                # If correction and error have the same sign, it's amplifying
                if (errors[ch] > 0 and corrections[ch] > 0) or \
                   (errors[ch] < 0 and corrections[ch] < 0):
                    positive_count += 1
        # Flag if more than half of channels show positive feedback
        if positive_count > len(errors) / 2:
            self.state.positive_feedback_detected = True

    def _update_set_points(self) -> None:
        """Apply allostatic drift to set points when error is chronic."""
        for channel in self._set_points:
            error = abs(self.state.errors.get(channel, 0.0))
            tolerance = self.config.tolerances.get(channel, 0.1)
            if error > tolerance * 2:
                # Chronic error → set point drifts toward the error
                drift = self.config.drift_rate * error
                self._set_points[channel] += drift
            elif error < tolerance * 0.5:
                # Low error → set point recovers toward original
                original = self.config.set_points[channel]
                current = self._set_points[channel]
                if abs(current - original) > 0.001:
                    recovery = self.config.recovery_rate * (original - current)
                    self._set_points[channel] += recovery

    @property
    def set_points(self) -> Dict[str, float]:
        return dict(self._set_points)

    def reset(self) -> None:
        """Reset the loop to initial state."""
        self.state = LoopState()
        self._set_points = dict(self.config.set_points)


# ---------------------------------------------------------------------------
# HomeostaticAgent — multi-loop agent with nested timescales
# ---------------------------------------------------------------------------

class HomeostaticAgent:
    """
    An agent whose self-regulation is governed by nested homeostatic loops
    at three timescales:

    - **Per-turn** (fast):   runs every agent step — immediate sensorimotor regulation
    - **Per-session** (medium): runs at session boundaries — behavior pattern regulation
    - **Cross-session** (slow):   runs across sessions — long-term adaptation / meta-learning

    This mirrors biological homeostasis where fast reflexes, intermediate
    hormonal regulation, and slow epigenetic adaptation operate simultaneously.
    """

    TIMESCALE_TURN = "per_turn"
    TIMESCALE_SESSION = "per_session"
    TIMESCALE_CROSS = "cross_session"

    def __init__(self, name: str = "HomeostaticAgent"):
        self.name = name
        self._loops: Dict[str, HomeostaticLoop] = {}
        self._loop_timescales: Dict[str, str] = {}
        self._session_count = 0
        self._turn_count = 0
        self._history: List[Dict] = []

    def add_loop(
        self,
        name: str,
        loop: HomeostaticLoop,
        timescale: str = TIMESCALE_TURN,
    ) -> None:
        """Register a homeostatic loop at a specific timescale."""
        assert timescale in (
            self.TIMESCALE_TURN,
            self.TIMESCALE_SESSION,
            self.TIMESCALE_CROSS,
        ), f"Unknown timescale: {timescale}"
        self._loops[name] = loop
        self._loop_timescales[name] = timescale

    # -- Agent execution ---------------------------------------------------

    def step(self) -> Dict[str, LoopState]:
        """Execute one agent step — runs per-turn loops."""
        self._turn_count += 1
        results = {}
        for name, loop in self._loops.items():
            if self._loop_timescales[name] == self.TIMESCALE_TURN:
                results[name] = loop.step()
        self._record_snapshot(results)
        return results

    def end_session(self) -> Dict[str, LoopState]:
        """
        Called at session boundaries — runs per-session loops and checks
        for allostatic overload.
        """
        self._session_count += 1
        results = {}
        for name, loop in self._loops.items():
            if self._loop_timescales[name] == self.TIMESCALE_SESSION:
                results[name] = loop.step()
        self._record_snapshot(results)
        return results

    def cross_session_update(self) -> Dict[str, LoopState]:
        """
        Called across sessions — runs cross-session loops for long-term
        adaptation (meta-learning, architecture changes).
        """
        results = {}
        for name, loop in self._loops.items():
            if self._loop_timescales[name] == self.TIMESCALE_CROSS:
                results[name] = loop.step()
        self._record_snapshot(results)
        return results

    # -- Inspection --------------------------------------------------------

    def get_allostatic_load_report(self) -> Dict[str, AllostaticLoadRecord]:
        """Return allostatic load for every loop."""
        return {
            name: loop.state.allostatic_load
            for name, loop in self._loops.items()
        }

    def has_positive_feedback_escape(self) -> Dict[str, bool]:
        """Check which loops have detected positive feedback escape."""
        return {
            name: loop.state.positive_feedback_detected
            for name, loop in self._loops.items()
        }

    def get_set_points(self) -> Dict[str, Dict[str, float]]:
        """Return current (possibly drifted) set points per loop."""
        return {
            name: loop.set_points
            for name, loop in self._loops.items()
        }

    def reset(self) -> None:
        """Reset agent to initial state."""
        for loop in self._loops.values():
            loop.reset()
        self._turn_count = 0
        self._session_count = 0
        self._history.clear()

    def _record_snapshot(self, results: Dict[str, LoopState]) -> None:
        self._history.append({
            "turn": self._turn_count,
            "session": self._session_count,
            "timestamp": time.time(),
            "loops": {
                name: {
                    "errors": dict(state.errors),
                    "positive_feedback": state.positive_feedback_detected,
                }
                for name, state in results.items()
            },
        })

    @property
    def turn_count(self) -> int:
        return self._turn_count

    @property
    def session_count(self) -> int:
        return self._session_count


# ---------------------------------------------------------------------------
# Factory helpers
# ---------------------------------------------------------------------------

def create_default_agent(name: str = "HomeostaticAgent") -> HomeostaticAgent:
    """
    Create a HomeostaticAgent with one loop per timescale using sensible defaults.
    """
    agent = HomeostaticAgent(name=name)

    # Per-turn loop: fast sensorimotor regulation
    turn_config = LoopConfig(
        set_points={"motor_error": 0.0, "activation": 0.5},
        tolerances={"motor_error": 0.05, "activation": 0.1},
        effector_bounds={"motor_error": (-0.5, 0.5), "activation": (-0.3, 0.3)},
        drift_rate=0.01,
        recovery_rate=0.005,
        name="per_turn_regulation",
    )
    agent.add_loop("per_turn", HomeostaticLoop(turn_config), HomeostaticAgent.TIMESCALE_TURN)

    # Per-session loop: medium-term behavioral regulation
    session_config = LoopConfig(
        set_points={"success_rate": 0.8, "exploration_rate": 0.2},
        tolerances={"success_rate": 0.1, "exploration_rate": 0.05},
        effector_bounds={"success_rate": (-0.2, 0.2), "exploration_rate": (-0.1, 0.1)},
        drift_rate=0.02,
        recovery_rate=0.01,
        name="per_session_regulation",
    )
    agent.add_loop("per_session", HomeostaticLoop(session_config), HomeostaticAgent.TIMESCALE_SESSION)

    # Cross-session loop: long-term meta-adaptation
    cross_config = LoopConfig(
        set_points={"architecture_complexity": 0.5, "learning_rate": 0.1},
        tolerances={"architecture_complexity": 0.1, "learning_rate": 0.02},
        effector_bounds={"architecture_complexity": (-0.1, 0.1), "learning_rate": (-0.05, 0.05)},
        drift_rate=0.005,
        recovery_rate=0.002,
        name="cross_session_adaptation",
    )
    agent.add_loop("cross_session", HomeostaticLoop(cross_config), HomeostaticAgent.TIMESCALE_CROSS)

    return agent
