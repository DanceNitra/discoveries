"""
neurobiology_agent_memory.main -- Complementary Learning Systems (CLS) Memory

Implements a 5-tier agent memory hierarchy inspired by mammalian neurobiology:

  Tier 1: Working Memory (PFC)          — transient scratchpad
  Tier 2: Episodic Buffer (Hippocampus) — fast, temporary, pattern-separated
  Tier 3: Semantic Store (Neocortex)    — slow, permanent, distributed
  Tier 4: Procedural (Basal Ganglia)    — habit/action chunks (sketch)
  Tier 5: Meta-Memory (PFC meta-cog)    — knowledge about memory itself

Core mechanism: Complementary Learning Systems (CLS) from McClelland et al. (1995).
EpisodicBuffer learns quickly without overwriting; SemanticStore slowly integrates
via offline replay consolidation. Strategic forgetting (TTL + salience pruning)
mirrors the binding problem and synaptic pruning.
"""

from __future__ import annotations

__version__ = "0.1.0"

import time
import math
import random
from typing import Any, Optional
from dataclasses import dataclass, field
from collections import defaultdict


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Episode:
    """A single episodic memory trace — fast-encoded, pattern-separated."""
    id: str
    content: dict[str, Any]
    salience: float            # 0.0 (trivial) to 1.0 (critical)
    created_at: float          # unix timestamp
    ttl: float                 # seconds until natural expiration
    consolidation_count: int = 0   # how many times replayed

    @property
    def is_expired(self) -> bool:
        return (time.time() - self.created_at) > self.ttl

    @property
    def age(self) -> float:
        return time.time() - self.created_at


@dataclass
class SemanticNode:
    """A consolidated, slowly-updated semantic memory node."""
    key: str
    value: Any
    strength: float            # 0.0 to 1.0, reflects consolidation weight
    last_accessed: float = 0.0
    created_at: float = 0.0


# ---------------------------------------------------------------------------
# Tier 2: Episodic Buffer (Hippocampus)
# ---------------------------------------------------------------------------

class EpisodicBuffer:
    """Fast-learning, temporary episodic store.

    Pattern-separation via content-hash addressing. Episodes have a TTL
    after which they are eligible for pruning. Capacity limit enforces
    the hippocampal binding problem — only so many concurrent patterns.
    """

    def __init__(self, capacity: int = 100, default_ttl: float = 3600.0):
        self.capacity = capacity
        self.default_ttl = default_ttl
        self._episodes: dict[str, Episode] = {}

    def encode(
        self,
        content: dict[str, Any],
        salience: float | None = None,
        ttl: float | None = None,
    ) -> str:
        """Encode a new episodic trace. Returns its id."""
        if len(self._episodes) >= self.capacity:
            self._prune_lowest_salience()

        ep_id = self._content_hash(content)
        if ep_id in self._episodes:
            # Re-encoding strengthens the existing trace
            self._episodes[ep_id].salience = max(
                self._episodes[ep_id].salience, salience or 0.5
            )
            self._episodes[ep_id].ttl = max(
                self._episodes[ep_id].ttl, ttl or self.default_ttl
            )
            return ep_id

        self._episodes[ep_id] = Episode(
            id=ep_id,
            content=dict(content),
            salience=salience if salience is not None else 0.5,
            created_at=time.time(),
            ttl=ttl if ttl is not None else self.default_ttl,
        )
        return ep_id

    def recall(self, ep_id: str) -> Optional[Episode]:
        ep = self._episodes.get(ep_id)
        if ep is None:
            return None
        if ep.is_expired:
            self.forget(ep_id)
            return None
        return ep

    def recall_by_similarity(self, query: dict, top_k: int = 5) -> list[Episode]:
        """Crude content-addressable recall by feature overlap."""
        scored: list[tuple[float, Episode]] = []
        now = time.time()
        for ep in self._episodes.values():
            if (now - ep.created_at) > ep.ttl:
                continue
            score = self._similarity(query, ep.content)
            scored.append((score, ep))
        scored.sort(key=lambda x: -x[0])
        return [ep for _, ep in scored[:top_k]]

    def forget(self, ep_id: str) -> bool:
        return self._episodes.pop(ep_id, None) is not None

    def strategic_forget(self, fraction: float = 0.2) -> int:
        """Prune expired + lowest salience episodes. Returns count removed."""
        count = 0
        now = time.time()
        # Remove expired
        expired = [eid for eid, ep in self._episodes.items()
                   if (now - ep.created_at) > ep.ttl]
        for eid in expired:
            del self._episodes[eid]
            count += 1
        # If still over capacity, remove lowest salience
        if len(self._episodes) > self.capacity:
            sorted_eps = sorted(
                self._episodes.items(), key=lambda x: x[1].salience
            )
            to_remove = sorted_eps[:int(len(sorted_eps) * fraction)]
            for eid, _ in to_remove:
                del self._episodes[eid]
                count += 1
        return count

    @property
    def size(self) -> int:
        return len(self._episodes)

    def _prune_lowest_salience(self) -> None:
        if not self._episodes:
            return
        lowest = min(self._episodes.items(), key=lambda x: x[1].salience)
        del self._episodes[lowest[0]]

    @staticmethod
    def _content_hash(content: dict) -> str:
        """Deterministic id based on content keys+values."""
        parts = sorted(f"{k}:{v}" for k, v in content.items())
        return hashlib_md5("|".join(parts))

    @staticmethod
    def _similarity(query: dict, target: dict) -> float:
        if not query or not target:
            return 0.0
        all_keys = set(query) | set(target)
        matches = sum(1 for k in all_keys if query.get(k) == target.get(k))
        return matches / len(all_keys)


# ---------------------------------------------------------------------------
# Tier 3: Semantic Store (Neocortex)
# ---------------------------------------------------------------------------

class SemanticStore:
    """Slow-learning, permanent semantic memory.

    Integration happens only during consolidation replay — analogous to
    neocortical slow-wave sleep upscaling. Strength decays very slowly
    unless reinforced.
    """

    def __init__(self, decay_rate: float = 0.001):
        self._nodes: dict[str, SemanticNode] = {}
        self.decay_rate = decay_rate

    def integrate(self, key: str, value: Any, strength_increment: float = 0.1) -> SemanticNode:
        """Integrate or reinforce a semantic memory node."""
        now = time.time()
        if key in self._nodes:
            node = self._nodes[key]
            node.value = value  # slow overwrite
            node.strength = min(1.0, node.strength + strength_increment)
            node.last_accessed = now
        else:
            self._nodes[key] = SemanticNode(
                key=key, value=value, strength=strength_increment,
                last_accessed=now, created_at=now,
            )
        return self._nodes[key]

    def query(self, key: str) -> Optional[Any]:
        node = self._nodes.get(key)
        if node is None:
            return None
        node.last_accessed = time.time()
        return node.value

    def query_by_strength(self, threshold: float = 0.3) -> list[SemanticNode]:
        return [n for n in self._nodes.values() if n.strength >= threshold]

    def decay(self) -> int:
        """Apply slow decay to all nodes. Returns number weakened below threshold."""
        pruned = 0
        for node in self._nodes.values():
            node.strength = max(0.0, node.strength - self.decay_rate)
            if node.strength < 0.01:
                pruned += 1
        return pruned

    def strategic_prune(self, threshold: float = 0.05) -> int:
        """Remove nodes whose strength has decayed below threshold."""
        keys = [k for k, n in self._nodes.items() if n.strength < threshold]
        for k in keys:
            del self._nodes[k]
        return len(keys)

    @property
    def size(self) -> int:
        return len(self._nodes)

    @property
    def total_strength(self) -> float:
        return sum(n.strength for n in self._nodes.values())


# ---------------------------------------------------------------------------
# Consolidation Engine
# ---------------------------------------------------------------------------

class MemoryConsolidator:
    """Offline replay from episodic buffer to semantic store.

    Models hippocampal sharp-wave ripple replay during NREM sleep.
    Options for stress-modulated prioritization (cortisol analog).
    """

    def __init__(self, replay_rate: float = 0.3, stress_level: float = 0.0):
        self.replay_rate = replay_rate       # fraction of episodes replayed per cycle
        self.stress_level = stress_level     # 0.0 (rest) to 1.0 (max stress)

    def consolidate(
        self,
        episodic: EpisodicBuffer,
        semantic: SemanticStore,
    ) -> dict[str, Any]:
        """Run one consolidation cycle. Returns stats."""
        stats = {
            "replayed": 0,
            "integrated": 0,
            "expired_skipped": 0,
            "salience_boost": 0.0,
        }

        # Gather replay candidates sorted by salience (stress biases toward salience)
        candidates = [
            ep for ep in episodic._episodes.values()
        ]

        # Stress modulation: under stress, replay favors high-salience episodes
        if self.stress_level > 0:
            stress_bias = 1.0 + self.stress_level * 2.0
            candidates.sort(
                key=lambda ep: ep.salience * stress_bias + random.random() * 0.1,
                reverse=True,
            )
        else:
            random.shuffle(candidates)

        replay_count = max(1, int(len(candidates) * self.replay_rate))

        for ep in candidates[:replay_count]:
            if ep.is_expired:
                stats["expired_skipped"] += 1
                continue

            # Extract key-value from content for semantic integration
            for k, v in ep.content.items():
                semantic_key = f"sem:{k}"
                # Strength increment proportional to salience
                increment = ep.salience * 0.2
                semantic.integrate(semantic_key, v, increment)
                stats["integrated"] += 1

            ep.consolidation_count += 1
            stats["replayed"] += 1
            stats["salience_boost"] += ep.salience

        return stats


# ---------------------------------------------------------------------------
# Full Agent Memory System
# ---------------------------------------------------------------------------

class MemoryAgent:
    """Unified 5-tier memory agent.

    Tiers:
      1. Working memory (scratchpad dict)
      2. EpisodicBuffer (hippocampus)
      3. SemanticStore (neocortex)
      4. Procedural (simple action-chunk registry)
      5. Meta-memory (introspective stats)

    Orchestrates encode → consolidate → strategic_forget cycle.
    """

    def __init__(
        self,
        episodic_capacity: int = 100,
        semantic_decay: float = 0.001,
        replay_rate: float = 0.3,
        stress_level: float = 0.0,
    ):
        self.working_memory: dict[str, Any] = {}
        self.episodic = EpisodicBuffer(capacity=episodic_capacity)
        self.semantic = SemanticStore(decay_rate=semantic_decay)
        self.procedural: dict[str, dict] = {}  # action chunks
        self.meta_memory: dict[str, Any] = {
            "total_encodes": 0,
            "total_consolidations": 0,
            "total_forgets": 0,
            "stress_level": stress_level,
        }
        self.consolidator = MemoryConsolidator(
            replay_rate=replay_rate, stress_level=stress_level,
        )
        self._cycle_count = 0

    def observe(self, content: dict, salience: float | None = None) -> str:
        """Observe an event — encode into working + episodic memory."""
        # Hold in working memory
        self.working_memory = dict(content)
        # Encode into episodic buffer
        ep_id = self.episodic.encode(content, salience=salience)
        self.meta_memory["total_encodes"] += 1
        return ep_id

    def recall_episodic(self, ep_id: str) -> Optional[Episode]:
        return self.episodic.recall(ep_id)

    def recall_semantic(self, key: str) -> Optional[Any]:
        return self.semantic.query(key)

    def run_cycle(self) -> dict[str, Any]:
        """One complete memory cycle: consolidate, decay, forget."""
        self._cycle_count += 1
        results = {}

        # 1. Consolidate
        consol_stats = self.consolidator.consolidate(self.episodic, self.semantic)
        self.meta_memory["total_consolidations"] += consol_stats["replayed"]
        results["consolidation"] = consol_stats

        # 2. Apply semantic decay
        decayed = self.semantic.decay()
        results["decayed"] = decayed

        # 3. Strategic forgetting on episodic buffer
        forgotten = self.episodic.strategic_forget(fraction=0.15)
        self.meta_memory["total_forgets"] += forgotten
        results["forgotten"] = forgotten

        # 4. Prune semantic store
        pruned = self.semantic.strategic_prune(threshold=0.02)
        results["semantic_pruned"] = pruned

        # 5. Update meta-memory
        results["meta"] = dict(self.meta_memory)
        results["episodic_size"] = self.episodic.size
        results["semantic_size"] = self.semantic.size

        return results

    def set_stress(self, level: float) -> None:
        """Adjust stress level for next consolidation cycle."""
        self.meta_memory["stress_level"] = level
        self.consolidator.stress_level = level

    def summary(self) -> dict[str, Any]:
        """Return a human-readable memory snapshot."""
        return {
            "working_memory": dict(self.working_memory),
            "episodic_count": self.episodic.size,
            "semantic_count": self.semantic.size,
            "procedural_count": len(self.procedural),
            "meta_memory": dict(self.meta_memory),
            "cycle_count": self._cycle_count,
        }


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def hashlib_md5(text: str) -> str:
    """Minimal pure-Python string hash (avoids hashlib dependency)."""
    # Uses Python's built-in hash with a stable seed-like transform
    h = 0
    for ch in text:
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    return f"ep_{h:08x}"
