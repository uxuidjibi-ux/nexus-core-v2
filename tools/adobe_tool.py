from typing import Any

from tools.base import BaseHTTPConnector


class AdobeTool(BaseHTTPConnector):
    def __init__(self, access_token: str, client_id: str, api_url: str, *, dry_run: bool = True):
        super().__init__(base_url=api_url, timeout=60, dry_run=dry_run)
        self._client.headers.update(
            {"Authorization": f"Bearer {access_token}", "x-api-key": client_id}
        )

    def generate_image(
        self, prompt: str, *, width: int = 1024, height: int = 1024, count: int = 1
    ) -> dict[str, Any]:
        payload = {
            "prompt": prompt,
            "size": {"width": width, "height": height},
            "n": max(1, min(count, 4)),
        }
        return self.request("POST", "", json=payload)
