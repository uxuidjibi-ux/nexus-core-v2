from typing import Any

from tools.base import BaseHTTPConnector


class FigmaTool(BaseHTTPConnector):
    """Figma REST is read-oriented; writes require a Figma plugin or approved endpoint."""

    def __init__(self, token: str, *, dry_run: bool = True):
        super().__init__(base_url="https://api.figma.com", dry_run=dry_run)
        self._client.headers["X-Figma-Token"] = token

    def get_file(self, file_key: str) -> dict[str, Any]:
        return self.request("GET", f"/v1/files/{file_key}")

    def get_components(self, file_key: str) -> dict[str, Any]:
        return self.request("GET", f"/v1/files/{file_key}/components")

    def post_plugin_manifest(self, webhook_url: str, manifest: dict[str, Any]) -> dict[str, Any]:
        # Plugin-side bridge: Figma REST itself cannot create arbitrary canvas nodes.
        with BaseHTTPConnector(dry_run=self.dry_run) as bridge:
            return bridge.request("POST", webhook_url, json={"manifest": manifest})
