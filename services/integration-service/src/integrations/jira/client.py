import httpx
from typing import List, Dict, Any, Optional
import base64

class JiraClient:
    def __init__(self, domain: str, email: str, api_token: str):
        self.base_url = f"https://{domain}.atlassian.net/rest/api/3"
        self.auth_header = self._get_auth_header(email, api_token)

    def _get_auth_header(self, email: str, api_token: str) -> str:
        auth_str = f"{email}:{api_token}"
        encoded_auth = base64.b64encode(auth_str.encode()).decode()
        return f"Basic {encoded_auth}"

    async def get_projects(self) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/project",
                headers={"Authorization": self.auth_header}
            )
            response.raise_for_status()
            return response.json()

    async def get_issues(self, project_key: str, jql: str = "") -> List[Dict[str, Any]]:
        query = f"project = {project_key}"
        if jql:
            query += f" AND {jql}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/search",
                params={"jql": query, "expand": "changelog"},
                headers={"Authorization": self.auth_header}
            )
            response.raise_for_status()
            return response.json().get("issues", [])

    async def get_issue(self, issue_key: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/issue/{issue_key}",
                headers={"Authorization": self.auth_header}
            )
            response.raise_for_status()
            return response.json()
