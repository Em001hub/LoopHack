from fastapi.testclient import TestClient
from src.main import app
import pytest

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["service"] == "integration-service"

def test_jira_endpoints_exist():
    # We expect 400 because credentials aren't set, but 404 would mean route missing
    response = client.get("/api/v1/jira/projects")
    assert response.status_code in [200, 400]

def test_github_endpoints_exist():
    response = client.get("/api/v1/github/repositories")
    assert response.status_code in [200, 400]

def test_slack_endpoints_exist():
    response = client.get("/api/v1/slack/channels")
    assert response.status_code in [200, 400]

def test_calendar_endpoints_exist():
    response = client.get("/api/v1/calendar/events")
    assert response.status_code in [200, 400]

if __name__ == "__main__":
    print("Running basic route verification...")
    test_health_check()
    test_jira_endpoints_exist()
    test_github_endpoints_exist()
    test_slack_endpoints_exist()
    test_calendar_endpoints_exist()
    print("All foundational routes are registered and active.")
