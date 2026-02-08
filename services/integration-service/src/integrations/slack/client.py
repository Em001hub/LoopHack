import httpx
from typing import List, Dict, Any, Optional

class SlackClient:
    def __init__(self, token: str):
        self.base_url = "https://slack.com/api"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8"
        }

    async def get_channels(self, types: str = "public_channel") -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/conversations.list",
                headers=self.headers,
                params={"types": types}
            )
            data = response.json()
            if not data.get("ok"):
                raise Exception(f"Slack API error: {data.get('error')}")
            return data.get("channels", [])

    async def get_messages(self, channel_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/conversations.history",
                headers=self.headers,
                params={"channel": channel_id, "limit": limit}
            )
            data = response.json()
            if not data.get("ok"):
                raise Exception(f"Slack API error: {data.get('error')}")
            return data.get("messages", [])

    async def get_users(self) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/users.list",
                headers=self.headers
            )
            data = response.json()
            if not data.get("ok"):
                raise Exception(f"Slack API error: {data.get('error')}")
            return data.get("members", [])
