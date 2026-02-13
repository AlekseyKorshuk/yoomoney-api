"""HTTP transport layer for the YooMoney API.

Provides both synchronous and asynchronous transports that handle
authentication, connection pooling, and request execution.
"""

from typing import Any, ClassVar

import httpx


class BaseTransport:
    """Shared configuration for sync / async transports."""

    DEFAULT_BASE_URL = "https://yoomoney.ru/api/"
    DEFAULT_HEADERS: ClassVar[dict[str, str]] = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    def __init__(self, token: str, base_url: str | None = None) -> None:
        self.token = token
        self.base_url = base_url or self.DEFAULT_BASE_URL

    def _auth_headers(self) -> dict[str, str]:
        return {**self.DEFAULT_HEADERS, "Authorization": f"Bearer {self.token}"}

    def _url(self, method: str) -> str:
        return self.base_url + method


class SyncTransport(BaseTransport):
    """Synchronous transport backed by :class:`httpx.Client`."""

    def __init__(self, token: str, base_url: str | None = None) -> None:
        super().__init__(token, base_url)
        self._client = httpx.Client(headers=self._auth_headers())

    def request(self, method: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
        response = self._client.post(self._url(method), data=data or {})
        result: dict[str, Any] = response.json()
        return result

    def close(self) -> None:
        self._client.close()


class AsyncTransport(BaseTransport):
    """Asynchronous transport backed by :class:`httpx.AsyncClient`."""

    def __init__(self, token: str, base_url: str | None = None) -> None:
        super().__init__(token, base_url)
        self._client = httpx.AsyncClient(headers=self._auth_headers())

    async def request(self, method: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
        response = await self._client.post(self._url(method), data=data or {})
        result: dict[str, Any] = response.json()
        return result

    async def close(self) -> None:
        await self._client.aclose()
