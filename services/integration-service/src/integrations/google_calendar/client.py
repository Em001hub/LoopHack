import httpx
from typing import List, Dict, Any, Optional

class GoogleCalendarClient:
    def __init__(self, api_key: Optional[str] = None, access_token: Optional[str] = None):
        self.base_url = "https://www.googleapis.com/calendar/v3"
        self.api_key = api_key
        self.access_token = access_token

    def _get_headers(self) -> Dict[str, str]:
        headers = {}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers

    def _get_params(self, params: Dict[str, Any] = None) -> Dict[str, Any]:
        if params is None:
            params = {}
        if self.api_key:
            params["key"] = self.api_key
        return params

    async def get_events(self, calendar_id: str = "primary", time_min: Optional[str] = None) -> List[Dict[str, Any]]:
        params = self._get_params()
        if time_min:
            params["timeMin"] = time_min

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/calendars/{calendar_id}/events",
                headers=self._get_headers(),
                params=params
            )
            response.raise_for_status()
            return response.json().get("items", [])
