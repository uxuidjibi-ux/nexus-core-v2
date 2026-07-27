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

    def build_case_study_manifest(
        self,
        *,
        project_name: str,
        language: str,
        slides: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Create a deterministic payload for the approved Figma plugin bridge."""
        if language not in {"fr", "en"}:
            raise ValueError("language must be 'fr' or 'en'")
        orders = [slide.get("order") for slide in slides]
        if orders != list(range(1, len(slides) + 1)):
            raise ValueError("slides must have contiguous order values starting at 1")
        return {
            "schema_version": "2.0",
            "operation": "create_case_study_deck",
            "project": project_name,
            "language": language,
            "canvas": {"width": 1920, "height": 1080, "ratio": "16:9"},
            "layout": {"engine": "auto-layout-v2", "mirror_key": project_name.casefold()},
            "slides": slides,
        }
