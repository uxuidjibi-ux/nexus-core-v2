from __future__ import annotations

from typing import Any

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential


class ConnectorError(RuntimeError):
    pass


class BaseHTTPConnector:
    def __init__(self, *, base_url: str = "", timeout: float = 20.0, dry_run: bool = True):
        self.base_url = base_url.rstrip("/")
        self.dry_run = dry_run
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=httpx.Timeout(timeout),
            follow_redirects=False,
            headers={"User-Agent": "NEXUS-CORE/2.0"},
        )

    def __enter__(self) -> BaseHTTPConnector:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        self._client.close()

    @retry(
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError)),
        wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    def request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        if self.dry_run and method.upper() not in {"GET", "HEAD", "OPTIONS"}:
            return {"dry_run": True, "method": method.upper(), "url": f"{self.base_url}{path}"}
        response = self._client.request(method, path, **kwargs)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise ConnectorError(
                f"API request failed ({response.status_code}) at {response.request.url}"
            ) from exc
        if not response.content:
            return {"status_code": response.status_code}
        data = response.json()
        return data if isinstance(data, dict) else {"data": data}
