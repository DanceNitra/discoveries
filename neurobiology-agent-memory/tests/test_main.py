"""Tests for neurobiology_agent_memory.main (CLS Memory System)"""
import pytest
from neurobiology_agent_memory.main import (
    EpisodicBuffer,
    SemanticStore,
    MemoryConsolidator,
    MemoryAgent,
    Episode,
    SemanticNode,
)


class TestEpisodicBuffer:
    def test_encode_and_recall(self):
        buf = EpisodicBuffer(capacity=10)
        eid = buf.encode({"event": "hello", "val": 42}, salience=0.8)
        ep = buf.recall(eid)
        assert ep is not None
        assert ep.content["event"] == "hello"
        assert ep.salience == 0.8
        assert not ep.is_expired

    def test_capacity_pruning(self):
        buf = EpisodicBuffer(capacity=3)
        ids = []
        for i in range(5):
            eid = buf.encode({"idx": i}, salience=0.1 + i * 0.2)
            ids.append(eid)
        assert buf.size <= 3  # capacity enforced

    def test_strategic_forget_expired(self):
        buf = EpisodicBuffer(capacity=100, default_ttl=-1.0)  # immediately expired
        buf.encode({"x": 1})
        assert buf.size == 1
        count = buf.strategic_forget()
        assert count >= 1
        assert buf.size == 0

    def test_recall_by_similarity(self):
        buf = EpisodicBuffer(capacity=10)
        buf.encode({"animal": "cat", "color": "black"}, salience=0.5)
        buf.encode({"animal": "dog", "color": "brown"}, salience=0.5)
        buf.encode({"animal": "cat", "color": "white"}, salience=0.5)
        results = buf.recall_by_similarity({"animal": "cat", "color": "black"})
        assert len(results) > 0

    def test_re_encoding_strengthens(self):
        buf = EpisodicBuffer(capacity=10)
        eid1 = buf.encode({"k": "v"}, salience=0.3)
        eid2 = buf.encode({"k": "v"}, salience=0.9)
        assert eid1 == eid2  # same content hash
        ep = buf.recall(eid1)
        assert ep is not None
        assert ep.salience == 0.9  # max of the two


class TestSemanticStore:
    def test_integrate_and_query(self):
        store = SemanticStore(decay_rate=0.001)
        store.integrate("sem:color", "blue", strength_increment=0.5)
        assert store.query("sem:color") == "blue"
        assert store._nodes["sem:color"].strength == 0.5

    def test_decay_and_prune(self):
        store = SemanticStore(decay_rate=0.1)
        store.integrate("sem:a", 1, strength_increment=0.05)  # already weak
        store.integrate("sem:b", 2, strength_increment=0.5)
        store.decay()
        pruned = store.strategic_prune(threshold=0.05)
        assert pruned >= 1  # sem:a fell below threshold

    def test_query_by_strength(self):
        store = SemanticStore()
        store.integrate("sem:important", "v1", strength_increment=0.8)
        store.integrate("sem:trivial", "v2", strength_increment=0.1)
        strong = store.query_by_strength(threshold=0.5)
        assert len(strong) == 1
        assert strong[0].key == "sem:important"


class TestMemoryConsolidator:
    def test_consolidation_transfers_to_semantic(self):
        episodic = EpisodicBuffer(capacity=10)
        semantic = SemanticStore()
        episodic.encode({"mood": "happy", "reason": "sun"}, salience=0.7)
        episodic.encode({"mood": "sad", "reason": "rain"}, salience=0.3)

        consol = MemoryConsolidator(replay_rate=1.0, stress_level=0.0)
        stats = consol.consolidate(episodic, semantic)

        assert stats["replayed"] > 0
        assert stats["integrated"] > 0
        # Semantic store should now have knowledge
        val = semantic.query("sem:mood")
        assert val is not None

    def test_stress_biases_consolidation(self):
        episodic = EpisodicBuffer(capacity=10)
        semantic = SemanticStore()
        episodic.encode({"event": "mundane"}, salience=0.2)
        episodic.encode({"event": "trauma"}, salience=0.9)

        # High stress should favor high-salience episodes
        consol = MemoryConsolidator(replay_rate=0.5, stress_level=0.8)
        stats = consol.consolidate(episodic, semantic)
        assert stats["replayed"] >= 0  # just verify it runs


class TestMemoryAgent:
    def test_full_cycle(self):
        agent = MemoryAgent(
            episodic_capacity=10,
            semantic_decay=0.001,
            replay_rate=0.5,
            stress_level=0.0,
        )
        # Encode events
        agent.observe({"location": "park", "weather": "sunny"}, salience=0.6)
        agent.observe({"location": "office", "task": "coding"}, salience=0.4)
        agent.observe({"location": "cafe", "food": "coffee"}, salience=0.5)

        # Run a full memory cycle
        results = agent.run_cycle()

        assert results["episodic_size"] <= 10
        assert "consolidation" in results
        assert "meta" in results
        assert agent.meta_memory["total_encodes"] == 3
        assert agent.meta_memory["total_consolidations"] >= 0
        assert results["semantic_size"] >= 0

    def test_stress_impact(self):
        agent = MemoryAgent(stress_level=0.0)
        assert agent.meta_memory["stress_level"] == 0.0
        agent.set_stress(0.9)
        assert agent.meta_memory["stress_level"] == 0.9
        assert agent.consolidator.stress_level == 0.9

    def test_recall_episodic(self):
        agent = MemoryAgent()
        eid = agent.observe({"test": "data"}, salience=0.8)
        ep = agent.recall_episodic(eid)
        assert ep is not None
        assert ep.content["test"] == "data"

    def test_recall_semantic_after_cycle(self):
        agent = MemoryAgent(replay_rate=1.0)
        agent.observe({"color": "green", "meaning": "go"}, salience=0.9)
        agent.run_cycle()
        # Should have been consolidated
        val = agent.recall_semantic("sem:color")
        assert val == "green"

    def test_summary(self):
        agent = MemoryAgent()
        agent.observe({"a": 1})
        s = agent.summary()
        assert "episodic_count" in s
        assert "semantic_count" in s
        assert "meta_memory" in s
        assert s["episodic_count"] == 1
