import json
import httpx
from datetime import datetime

API_BASE_URL = "http://127.0.0.1:8000"

def test_get_endpoints():
    """
    Tests all active GET endpoints to verify that the seeded database
    records are correctly being served by the FastAPI gateway.
    """
    print("\n=== STARTING GET ENDPOINT TESTS ===")
    
    # 1. Test GET /candidates
    print("\nTesting: GET /candidates ...")
    try:
        response = httpx.get(f"{API_BASE_URL}/candidates", timeout=5.0)
        if response.status_code == 200:
            candidates = response.json()
            print(f"✅ SUCCESS: Successfully fetched {len(candidates)} candidates.")
            if candidates:
                print(f"   👉 First Candidate: {candidates[0].get('name')} ({candidates[0].get('id')})")
        else:
            print(f"❌ FAILED: GET /candidates returned status code {response.status_code}")
    except Exception as e:
        print(f"❌ CONNECTION ERROR: Could not connect to API server. Is Uvicorn running? Details: {e}")
        return False

    # 2. Test GET /candidate/{id}
    print("\nTesting: GET /candidate/1 ...")
    try:
        response = httpx.get(f"{API_BASE_URL}/candidate/1", timeout=5.0)
        if response.status_code == 200:
            candidate = response.json()
            if candidate and candidate.get("id") == 1:
                print(f"✅ SUCCESS: Fetched candidate 1: {candidate.get('name')}")
            else:
                print(f"⚠️ WARNING: Endpoint returned but candidate ID 1 doesn't match.")
        else:
            print(f"❌ FAILED: GET /candidate/1 returned status code {response.status_code}")
    except Exception as e:
        print(f"❌ ERROR: {e}")

    # 3. Test GET /jobs
    print("\nTesting: GET /jobs ...")
    try:
        response = httpx.get(f"{API_BASE_URL}/jobs", timeout=5.0)
        if response.status_code == 200:
            jobs = response.json()
            print(f"✅ SUCCESS: Successfully fetched {len(jobs)} jobs.")
            if jobs:
                print(f"   👉 First Job: '{jobs[0].get('job_title')}' at {jobs[0].get('company')}")
        else:
            print(f"❌ FAILED: GET /jobs returned status code {response.status_code}")
    except Exception as e:
        print(f"❌ ERROR: {e}")

    # 4. Test GET /job/{id}
    print("\nTesting: GET /job/1 ...")
    try:
        response = httpx.get(f"{API_BASE_URL}/job/1", timeout=5.0)
        if response.status_code == 200:
            job = response.json()
            if job and job.get("id") == 1:
                print(f"✅ SUCCESS: Fetched job 1: '{job.get('job_title')}'")
            else:
                print(f"⚠️ WARNING: Endpoint returned but job ID 1 doesn't match.")
        else:
            print(f"❌ FAILED: GET /job/1 returned status code {response.status_code}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    return True

def test_evaluation_endpoints():
    """
    Simulates writing a structured evaluation payload, then attempts
    a secondary write to test the API's internal duplicate/overwrite guards.
    """
    print("\n=== STARTING POST EVALUATION TESTS ===")
    
    evaluation_payload = {
        "job_id": 1,
        "candidate_id": 1,
        "overall_score": 85,
        "decision": "Proceed",
        "strengths": ["Strong FastAPI experience", "Docker packaging skills"],
        "missing_skills": ["Kubernetes orchestration"],
        "reasoning": "Candidate possesses great backend skills matching 80% of our tech stack.",
        "summary": "Highly recommended for active backend position.",
        "evaluated_at": datetime.now().isoformat(),
        "run_id": "test_run_01"
    }
    
    # 5. POST /save-evaluation (Initial Save)
    print("\nTesting: POST /save-evaluation (Initial Save) ...")
    try:
        response = httpx.post(f"{API_BASE_URL}/save-evaluation", json=evaluation_payload, timeout=5.0)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS: Saved new evaluation. Server response: {result}")
        else:
            print(f"❌ FAILED: POST /save-evaluation returned status code {response.status_code}")
            print(f"   Response Body: {response.text}")
            return
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return

    # 6. POST /save-evaluation (Test Idempotency Guard/Duplicate Block)
    print("\nTesting: POST /save-evaluation (Duplicate Verification) ...")
    try:
        response = httpx.post(f"{API_BASE_URL}/save-evaluation", json=evaluation_payload, timeout=5.0)
        if response.status_code == 200:
            result = response.json()
            # If the database guard successfully intercepts the duplicate, status will be 'skipped'
            if result.get("status") == "skipped":
                print(f"✅ SUCCESS: Idempotency guard working. Duplicate write intercepted cleanly!")
                print(f"   Server message: '{result.get('message')}'")
            else:
                print(f"⚠️ WARNING: Write went through instead of skipping. Response: {result}")
        else:
            print(f"❌ FAILED: POST /save-evaluation duplicate block returned status {response.status_code}")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    print("=============================================")
    print(" N8N API INTEGRATION SUITE ")
    print("=============================================")
    
    server_healthy = test_get_endpoints()
    if server_healthy:
        test_evaluation_endpoints()
        
    print("\n=============================================")
    print(" Suite complete.")
    print("=============================================")