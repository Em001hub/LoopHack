#!/usr/bin/env python3
"""
Demo Endpoints Script for ProjectMind Intelligence Service
Tests all endpoints with beautiful terminal output
"""

import requests
import json
import time
import os
import sys
from datetime import datetime

# ANSI color codes
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# API configuration
BASE_URL = os.getenv("INTELLIGENCE_API_URL", "http://localhost:4002")


def print_header(title):
    """Print a section header"""
    print(f"\n{Colors.CYAN}{'═' * 60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{title.center(60)}{Colors.ENDC}")
    print(f"{Colors.CYAN}{'═' * 60}{Colors.ENDC}\n")


def print_endpoint(method, path, description):
    """Print endpoint info"""
    method_color = Colors.GREEN if method == "GET" else Colors.YELLOW
    print(f"{method_color}{method:6}{Colors.ENDC} {Colors.BLUE}{path}{Colors.ENDC}")
    print(f"       {Colors.HEADER}{description}{Colors.ENDC}")


def print_result(success, message, data=None):
    """Print endpoint result"""
    if success:
        print(f"  {Colors.GREEN}✓ {message}{Colors.ENDC}")
    else:
        print(f"  {Colors.RED}✗ {message}{Colors.ENDC}")
    
    if data:
        formatted = json.dumps(data, indent=2, default=str)
        for line in formatted.split('\n')[:10]:  # Limit output
            print(f"       {line}")
        if formatted.count('\n') > 10:
            print(f"       ... (truncated)")


def test_health():
    """Test health endpoints"""
    print_header("🏥 HEALTH ENDPOINTS")
    
    # Health check
    print_endpoint("GET", "/health", "Basic health check")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print_result(
            response.status_code == 200,
            f"Status: {response.status_code}",
            response.json() if response.status_code == 200 else None
        )
    except Exception as e:
        print_result(False, f"Error: {e}")
    
    print()
    
    # Project health
    print_endpoint("GET", "/api/v1/project-health/{project_id}", "Project health score")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/project-health/proj_alpha", timeout=10)
        print_result(
            response.status_code in [200, 404],
            f"Status: {response.status_code}",
            response.json() if response.status_code == 200 else None
        )
    except Exception as e:
        print_result(False, f"Error: {e}")


def test_predictions():
    """Test prediction endpoints"""
    print_header("📊 PREDICTION ENDPOINTS")
    
    # Timeline prediction
    print_endpoint("POST", "/api/v1/predict-timeline", "Predict project timeline")
    try:
        payload = {"project_id": "proj_alpha", "include_confidence": True}
        response = requests.post(f"{BASE_URL}/api/v1/predict-timeline", json=payload, timeout=10)
        print_result(
            response.status_code == 200,
            f"Status: {response.status_code}",
            response.json() if response.status_code == 200 else None
        )
    except Exception as e:
        print_result(False, f"Error: {e}")
    
    print()
    
    # Prediction history
    print_endpoint("GET", "/api/v1/prediction-history/{project_id}", "Get prediction history")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/prediction-history/proj_alpha", timeout=10)
        print_result(
            response.status_code in [200, 404],
            f"Status: {response.status_code}",
            response.json() if response.status_code == 200 else None
        )
    except Exception as e:
        print_result(False, f"Error: {e}")
    
    print()
    
    # Recalculate timeline
    print_endpoint("POST", "/api/v1/recalculate-timeline/{project_id}", "Background recalculation")
    try:
        response = requests.post(f"{BASE_URL}/api/v1/recalculate-timeline/proj_alpha", timeout=10)
        print_result(
            response.status_code in [200, 202],
            f"Status: {response.status_code}",
            response.json() if response.status_code in [200, 202] else None
        )
    except Exception as e:
        print_result(False, f"Error: {e}")


def test_skills():
    """Test skill endpoints"""
    print_header("🎯 SKILL ENDPOINTS")
    
    # Extract skills
    print_endpoint("POST", "/api/v1/extract-skills", "Extract user skills")
    try:
        payload = {"user_id": "user_sarah", "days": 90}
        response = requests.post(f"{BASE_URL}/api/v1/extract-skills", json=payload, timeout=15)
        print_result(
            response.status_code in [200, 422],
            f"Status: {response.status_code}",
            response.json() if response.status_code == 200 else None
        )
    except Exception as e:
        print_result(False, f"Error: {e}")
    
    print()
    
    # Get cached skills
    print_endpoint("GET", "/api/v1/skills/{user_id}", "Get cached skills")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/skills/user_sarah", timeout=10)
        print_result(
            response.status_code in [200, 404],
            f"Status: {response.status_code}",
            response.json() if response.status_code == 200 else None
        )
    except Exception as e:
        print_result(False, f"Error: {e}")
    
    print()
    
    # Match task
    print_endpoint("POST", "/api/v1/match-task", "Match task to skills")
    try:
        payload = {"task_id": "task_001", "required_skills": ["python", "fastapi"]}
        response = requests.post(f"{BASE_URL}/api/v1/match-task", json=payload, timeout=10)
        print_result(
            response.status_code in [200, 422],
            f"Status: {response.status_code}",
            response.json() if response.status_code == 200 else None
        )
    except Exception as e:
        print_result(False, f"Error: {e}")
    
    print()
    
    # Team skills
    print_endpoint("GET", "/api/v1/team-skills/{project_id}", "Team skill matrix")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/team-skills/proj_alpha", timeout=10)
        print_result(
            response.status_code in [200, 404],
            f"Status: {response.status_code}",
            response.json() if response.status_code == 200 else None
        )
    except Exception as e:
        print_result(False, f"Error: {e}")
    
    print()
    
    # Recommend assignment
    print_endpoint("POST", "/api/v1/recommend-assignment/{task_id}", "AI assignment recommendations")
    try:
        response = requests.post(f"{BASE_URL}/api/v1/recommend-assignment/task_001", timeout=10)
        print_result(
            response.status_code in [200, 404, 422],
            f"Status: {response.status_code}",
            response.json() if response.status_code == 200 else None
        )
    except Exception as e:
        print_result(False, f"Error: {e}")


def test_simulations():
    """Test simulation endpoints"""
    print_header("🎲 SIMULATION ENDPOINTS")
    
    # Monte Carlo simulation
    print_endpoint("POST", "/api/v1/simulate-timeline", "Monte Carlo simulation")
    try:
        payload = {"project_id": "proj_alpha", "n_simulations": 100}
        response = requests.post(f"{BASE_URL}/api/v1/simulate-timeline", json=payload, timeout=30)
        print_result(
            response.status_code in [200, 422],
            f"Status: {response.status_code}",
            response.json() if response.status_code == 200 else None
        )
    except Exception as e:
        print_result(False, f"Error: {e}")
    
    print()
    
    # Compare scenarios
    print_endpoint("POST", "/api/v1/compare-scenarios", "Scenario comparison")
    try:
        payload = {
            "project_id": "proj_alpha",
            "scenarios": [
                {"name": "baseline"},
                {"name": "add_developer", "add_developers": 1}
            ]
        }
        response = requests.post(f"{BASE_URL}/api/v1/compare-scenarios", json=payload, timeout=30)
        print_result(
            response.status_code in [200, 422],
            f"Status: {response.status_code}",
            response.json() if response.status_code == 200 else None
        )
    except Exception as e:
        print_result(False, f"Error: {e}")
    
    print()
    
    # What-if analysis
    print_endpoint("POST", "/api/v1/what-if/{project_id}", "Quick what-if analysis")
    try:
        payload = {"add_developers": 2, "remove_tasks": 0}
        response = requests.post(f"{BASE_URL}/api/v1/what-if/proj_alpha", json=payload, timeout=15)
        print_result(
            response.status_code in [200, 422],
            f"Status: {response.status_code}",
            response.json() if response.status_code == 200 else None
        )
    except Exception as e:
        print_result(False, f"Error: {e}")


def test_sentiment():
    """Test sentiment endpoints"""
    print_header("😊 SENTIMENT ENDPOINTS")
    
    # Analyze user sentiment
    print_endpoint("POST", "/api/v1/analyze-user", "User sentiment analysis")
    try:
        payload = {"user_id": "user_sarah", "days": 30}
        response = requests.post(f"{BASE_URL}/api/v1/analyze-user", json=payload, timeout=15)
        print_result(
            response.status_code in [200, 422],
            f"Status: {response.status_code}",
            response.json() if response.status_code == 200 else None
        )
    except Exception as e:
        print_result(False, f"Error: {e}")
    
    print()
    
    # Team morale
    print_endpoint("GET", "/api/v1/team-morale/{project_id}", "Team morale")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/team-morale/proj_alpha", timeout=10)
        print_result(
            response.status_code in [200, 404],
            f"Status: {response.status_code}",
            response.json() if response.status_code == 200 else None
        )
    except Exception as e:
        print_result(False, f"Error: {e}")
    
    print()
    
    # Burnout risk
    print_endpoint("GET", "/api/v1/burnout-risk/{user_id}", "Burnout risk check")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/burnout-risk/user_sarah", timeout=10)
        print_result(
            response.status_code in [200, 404],
            f"Status: {response.status_code}",
            response.json() if response.status_code == 200 else None
        )
    except Exception as e:
        print_result(False, f"Error: {e}")
    
    print()
    
    # Sentiment alerts
    print_endpoint("GET", "/api/v1/sentiment-alerts/{project_id}", "Active alerts")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/sentiment-alerts/proj_alpha", timeout=10)
        print_result(
            response.status_code in [200, 404],
            f"Status: {response.status_code}",
            response.json() if response.status_code == 200 else None
        )
    except Exception as e:
        print_result(False, f"Error: {e}")


def test_insights():
    """Test insights endpoints"""
    print_header("💡 INSIGHTS ENDPOINTS")
    
    # Daily insights
    print_endpoint("GET", "/api/v1/daily-insights/{project_id}", "Daily insights")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/daily-insights/proj_alpha", timeout=10)
        print_result(
            response.status_code in [200, 404],
            f"Status: {response.status_code}",
            response.json() if response.status_code == 200 else None
        )
    except Exception as e:
        print_result(False, f"Error: {e}")
    
    print()
    
    # Task recommendations
    print_endpoint("GET", "/api/v1/recommendations/{task_id}", "Task recommendations")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/recommendations/task_001", timeout=10)
        print_result(
            response.status_code in [200, 404],
            f"Status: {response.status_code}",
            response.json() if response.status_code == 200 else None
        )
    except Exception as e:
        print_result(False, f"Error: {e}")


def main():
    """Run all endpoint demos"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║     🧠 ProjectMind Intelligence Service - Endpoint Demo        ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")
    
    print(f"\n{Colors.YELLOW}Testing API at: {BASE_URL}{Colors.ENDC}")
    print(f"{Colors.YELLOW}Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
    
    start_time = time.time()
    
    # Run all tests
    test_health()
    test_predictions()
    test_skills()
    test_simulations()
    test_sentiment()
    test_insights()
    
    # Summary
    elapsed = time.time() - start_time
    print_header("📋 SUMMARY")
    print(f"{Colors.GREEN}Demo completed in {elapsed:.2f} seconds{Colors.ENDC}")
    print(f"\n{Colors.BOLD}API Documentation:{Colors.ENDC} {BASE_URL}/docs")
    print(f"{Colors.BOLD}Health Endpoint:{Colors.ENDC} {BASE_URL}/health")
    print()


if __name__ == "__main__":
    main()
