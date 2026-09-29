import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.server import app
from fastapi.testclient import TestClient

def main():
    print("Testing MemoryGuard Backend API...")
    client = TestClient(app)
    
    # 1. Health
    res = client.get("/api/health")
    assert res.status_code == 200, f"Health failed: {res.text}"
    print("[PASS] GET /api/health ->", res.json()["status"])
    
    # 2. Deals
    res = client.get("/api/deals")
    assert res.status_code == 200, f"Deals failed: {res.text}"
    deals = res.json()["deals"]
    print(f"[PASS] GET /api/deals -> {len(deals)} deals found")
    
    # 3. Single Deal
    res = client.get("/api/deals/acme")
    assert res.status_code == 200, f"Get single deal failed: {res.text}"
    print("[PASS] GET /api/deals/acme ->", res.json()["deal"]["name"])
    
    # 4. Memories
    res = client.get("/api/memories")
    assert res.status_code == 200, f"Memories failed: {res.text}"
    print(f"[PASS] GET /api/memories -> {res.json()['total']} memories")
    
    # 5. Outcomes
    res = client.get("/api/outcomes")
    assert res.status_code == 200, f"Outcomes failed: {res.text}"
    print(f"[PASS] GET /api/outcomes -> {res.json()['total']} outcomes")
    
    # 6. Evaluation
    res = client.get("/api/evaluation")
    assert res.status_code == 200, f"Evaluation failed: {res.text}"
    print("[PASS] GET /api/evaluation -> Contamination rejection rate:", res.json()["metrics"]["contamination_rejection_rate"])
    
    # 7. Audit
    res = client.get("/api/audit")
    assert res.status_code == 200, f"Audit failed: {res.text}"
    print(f"[PASS] GET /api/audit -> {len(res.json()['audit_events'])} events")
    
    print("\nALL BACKEND API CONTRACT TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
