from typing import Any, Literal

from tools.base import BaseHTTPConnector


class ReadyAITool(BaseHTTPConnector):
    def __init__(self, webhook_url: str, api_key: str | None = None, *, dry_run: bool = True):
        super().__init__(dry_run=dry_run)
        self.webhook_url = webhook_url
        if api_key:
            self._client.headers["Authorization"] = f"Bearer {api_key}"

    def trigger(
        self,
        event: Literal["content.ready", "site.deploy", "asset.ready"],
        payload: dict[str, Any],
        idempotency_key: str,
    ) -> dict[str, Any]:
        headers = {"Idempotency-Key": idempotency_key}
        return self.request(
            "POST", self.webhook_url, json={"event": event, "payload": payload}, headers=headers
        )
