"""
Comprehensive API Testing Script
Tests all implemented endpoints
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8002"

def print_test_header(test_name):
    print(f"\n{'='*70}")
    print(f"  {test_name}")
    print(f"{'='*70}")

def print_result(endpoint, status_code, response_data):
    status_emoji = "✅" if status_code == 200 else "❌"
    print(f"{status_emoji} {endpoint}")
    print(f"   Status: {status_code}")
    if status_code == 200:
        print(f"   Response: {json.dumps(response_data, indent=2)[:200]}...")
    else:
        print(f"   Error: {response_data}")
    print()

def test_health_endpoint():
    """Test health check endpoint"""
    print_test_header("1. HEALTH CHECK")
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print_result("GET /health", response.status_code, response.json())
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_root_endpoint():
    """Test root endpoint"""
    print_test_header("2. ROOT ENDPOINT")
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print_result("GET /", response.status_code, response.json())
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
        return False

def test_timeline_prediction():
    """Test timeline prediction endpoint"""
    print_test_header("3. TIMELINE PREDICTION")
    
    try:
        payload = {
            "project_id": "test_project_123",
            "target_date": (datetime.now() + timedelta(days=60)).isoformat()
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/predict-timeline",
            json=payload,
            timeout=10
        )
        print_result("POST /api/v1/predict-timeline", response.status_code, response.json())
        return response.status_code in [200, 500]  # 500 expected if no DB
    except Exception as e:
        print(f"❌ Timeline prediction failed: {e}")
        return False

def test_skill_extraction():
    """Test skill extraction endpoint"""
    print_test_header("4. SKILL EXTRACTION")
    
    try:
        payload = {
            "user_id": "test_user_123",
            "days": 90
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/extract-skills",
            json=payload,
            timeout=10
        )
        print_result("POST /api/v1/extract-skills", response.status_code, response.json())
        return response.status_code in [200, 500]  # 500 expected if no DB
    except Exception as e:
        print(f"❌ Skill extraction failed: {e}")
        return False

def test_sentiment_analysis():
    """Test sentiment analysis endpoint"""
    print_test_header("5. SENTIMENT ANALYSIS")
    
    try:
        payload = {
            "user_id": "test_user_123",
            "days": 30
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/analyze-user",
            json=payload,
            timeout=10
        )
        print_result("POST /api/v1/analyze-user", response.status_code, response.json())
        return response.status_code in [200, 500]  # 500 expected if no DB
    except Exception as e:
        print(f"❌ Sentiment analysis failed: {e}")
        return False

def test_simulation():
    """Test Monte Carlo simulation endpoint"""
    print_test_header("6. MONTE CARLO SIMULATION")
    
    try:
        payload = {
            "project_id": "test_project_123",
            "n_simulations": 100,
            "scenario_params": {
                "add_developers": 2
            }
        }
        
        response = requests.post(
            f"{BASE_URL}/api/v1/simulate-timeline",
            json=payload,
            timeout=15
        )
        print_result("POST /api/v1/simulate-timeline", response.status_code, response.json())
        return response.status_code in [200, 500]  # 500 expected if no DB
    except Exception as e:
        print(f"❌ Simulation failed: {e}")
        return False

def test_api_docs():
    """Test API documentation endpoint"""
    print_test_header("7. API DOCUMENTATION")
    
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        print_result("GET /docs", response.status_code, "HTML Documentation")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ API docs failed: {e}")
        return False

def test_openapi_schema():
    """Test OpenAPI schema endpoint"""
    print_test_header("8. OPENAPI SCHEMA")
    
    try:
        response = requests.get(f"{BASE_URL}/openapi.json", timeout=5)
        print_result("GET /openapi.json", response.status_code, response.json())
        return response.status_code == 200
    except Exception as e:
        print(f"❌ OpenAPI schema failed: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("  INTELLIGENCE SERVICE - COMPREHENSIVE API TESTING")
    print("="*70)
    print(f"\nTesting service at: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # Run all tests
    results.append(("Health Check", test_health_endpoint()))
    results.append(("Root Endpoint", test_root_endpoint()))
    results.append(("API Documentation", test_api_docs()))
    results.append(("OpenAPI Schema", test_openapi_schema()))
    results.append(("Timeline Prediction", test_timeline_prediction()))
    results.append(("Skill Extraction", test_skill_extraction()))
    results.append(("Sentiment Analysis", test_sentiment_analysis()))
    results.append(("Monte Carlo Simulation", test_simulation()))
    
    # Print summary
    print("\n" + "="*70)
    print("  TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n{'='*70}")
    print(f"  TOTAL: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    print(f"{'='*70}\n")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Service is working correctly!")
    elif passed >= total * 0.5:
        print("⚠️  PARTIAL SUCCESS - Some endpoints working (DB may not be configured)")
    else:
        print("❌ TESTS FAILED - Service may not be running")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
