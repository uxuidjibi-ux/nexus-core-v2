from typing import Any, Literal

from tools.base import BaseHTTPConnector


class WordPressTool(BaseHTTPConnector):
    def __init__(self, url: str, username: str, app_password: str, *, dry_run: bool = True):
        super().__init__(base_url=f"{url.rstrip('/')}/wp-json", dry_run=dry_run)
        self._client.auth = (username, app_password)

    def create_post(
        self,
        title: str,
        content: str,
        *,
        status: Literal["draft", "pending", "private", "publish"] = "draft",
        post_type: str = "posts",
        slug: str | None = None,
        meta: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if status == "publish" and self.dry_run:
            status = "draft"
        payload: dict[str, Any] = {"title": title, "content": content, "status": status}
        if slug:
            payload["slug"] = slug
        if meta:
            payload["meta"] = meta
        return self.request("POST", f"/wp/v2/{post_type}", json=payload)

    def update_post(self, post_id: int, payload: dict[str, Any], post_type: str = "posts"):
        return self.request("POST", f"/wp/v2/{post_type}/{post_id}", json=payload)

    def list_content(self, post_type: str = "posts", per_page: int = 10):
        return self.request("GET", f"/wp/v2/{post_type}", params={"per_page": per_page})
