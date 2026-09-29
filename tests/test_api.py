import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.server import app

client = TestClient(app)


def test_health_endpoint():
    """Verify system health endpoint returns 200 and healthy status."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["backend"] == "CONNECTED"
    assert "models" in data
    assert "thresholds" in data


def test_list_deals_endpoint():
    """Verify deals listing returns demo deals and correct summary metrics."""
    response = client.get("/api/deals")
    assert response.status_code == 200
    data = response.json()
    assert "deals" in data
    assert len(data["deals"]) >= 5
    assert data["total_pipeline_value"] > 0
    assert any(d["id"] == "acme" for d in data["deals"])
    assert any(d["id"] == "northwind" for d in data["deals"])


def test_get_single_deal():
    """Verify single deal endpoint returns deal info and conversation."""
    response = client.get("/api/deals/acme")
    assert response.status_code == 200
    data = response.json()
    assert data["deal"]["id"] == "acme"
    assert data["deal"]["name"] == "Acme Corp"
    assert "conversation" in data


def test_get_nonexistent_deal():
    """Verify 404 for invalid deal."""
    response = client.get("/api/deals/invalid-deal-123")
    assert response.status_code == 404


def test_memories_endpoint():
    """Verify memories query endpoint returns project and common memories."""
    response = client.get("/api/memories")
    assert response.status_code == 200
    data = response.json()
    assert "memories" in data
    assert isinstance(data["memories"], list)


def test_outcomes_endpoint():
    """Verify outcomes endpoint returns verified outcome records and learning timeline."""
    response = client.get("/api/outcomes")
    assert response.status_code == 200
    data = response.json()
    assert "outcomes" in data
    assert "learning_timeline" in data
    assert "learning_impact" in data


def test_evaluation_benchmark_endpoint():
    """Verify evaluation benchmark endpoint returns metrics and ablation table."""
    response = client.get("/api/evaluation")
    assert response.status_code == 200
    data = response.json()
    assert "metrics" in data
    assert "ablation_table" in data
    assert "scenario_evaluations" in data
    assert data["metrics"]["contamination_rejection_rate"] == 1.0


def test_audit_trail_endpoint():
    """Verify audit trail endpoint returns chronological governance events."""
    response = client.get("/api/audit")
    assert response.status_code == 200
    data = response.json()
    assert "audit_events" in data
    assert len(data["audit_events"]) > 0


def test_deal_turn_processing():
    """Verify turn processing executes agent loop and MemoryGuard verification."""
    payload = {
        "user_input": "I prefer email for all deal communication",
        "customer_name": "Acme Corp",
        "deal_stage": "Evaluation"
    }
    response = client.post("/api/deals/acme/turn", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "memory_decisions" in data
    assert "turn_id" in data
    assert data["deal_id"] == "acme"


def test_demo_user_endpoint():
    """Verify demo user authentication info."""
    response = client.get("/api/auth/demo-user")
    assert response.status_code == 200
    data = response.json()
    assert data["uid"] == "rep-001"
    assert "email" in data
