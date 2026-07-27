from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from tools.base import BaseHTTPConnector


class DriveTool(BaseHTTPConnector):
    """Minimal Google Drive v3 connector with mutations protected by dry-run."""

    def __init__(self, access_token: str, *, dry_run: bool = True):
        super().__init__(base_url="https://www.googleapis.com", timeout=60, dry_run=dry_run)
        self._client.headers["Authorization"] = f"Bearer {access_token}"

    def list_files(
        self,
        *,
        query: str | None = None,
        page_size: int = 100,
        fields: str = "files(id,name,mimeType,parents,webViewLink)",
    ) -> dict[str, Any]:
        params: dict[str, Any] = {
            "pageSize": max(1, min(page_size, 1000)),
            "fields": fields,
            "supportsAllDrives": "true",
            "includeItemsFromAllDrives": "true",
        }
        if query:
            params["q"] = query
        return self.request("GET", "/drive/v3/files", params=params)

    def create_folder(self, name: str, *, parent_id: str | None = None) -> dict[str, Any]:
        metadata: dict[str, Any] = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
        }
        if parent_id:
            metadata["parents"] = [parent_id]
        return self.request(
            "POST",
            "/drive/v3/files",
            params={"fields": "id,name,parents,webViewLink"},
            json=metadata,
        )

    def upload_document(
        self,
        source: Path,
        *,
        name: str | None = None,
        parent_id: str | None = None,
        language: Literal["fr", "en"],
    ) -> dict[str, Any]:
        """Prepare a Drive upload; binary transfer is explicit and dry-run by default."""
        resolved = source.resolve()
        if not resolved.is_file():
            raise FileNotFoundError(resolved)
        metadata: dict[str, Any] = {
            "name": name or resolved.name,
            "appProperties": {"nexusLanguage": language},
        }
        if parent_id:
            metadata["parents"] = [parent_id]
        if self.dry_run:
            return {
                "dry_run": True,
                "operation": "upload_document",
                "source": str(resolved),
                "metadata": metadata,
            }
        with resolved.open("rb") as file_handle:
            files = {
                "metadata": (
                    None,
                    __import__("json").dumps(metadata),
                    "application/json; charset=UTF-8",
                ),
                "file": (resolved.name, file_handle, "application/octet-stream"),
            }
            return self.request(
                "POST",
                "/upload/drive/v3/files",
                params={"uploadType": "multipart", "fields": "id,name,parents,webViewLink"},
                files=files,
            )

    def move_file(
        self,
        file_id: str,
        *,
        destination_parent_id: str,
        current_parent_id: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, str] = {
            "addParents": destination_parent_id,
            "fields": "id,name,parents,webViewLink",
        }
        if current_parent_id:
            params["removeParents"] = current_parent_id
        return self.request("PATCH", f"/drive/v3/files/{file_id}", params=params)
