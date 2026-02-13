from datetime import datetime
from types import TracebackType

from yoomoney._parsers import (
    build_history_payload,
    parse_account,
    parse_history,
    parse_operation_details,
)
from yoomoney._transport import AsyncTransport
from yoomoney.account.account import Account
from yoomoney.history.history import History
from yoomoney.operation_details.operation_details import OperationDetails


class AsyncClient:
    """Asynchronous YooMoney API client."""

    def __init__(
        self,
        token: str | None = None,
        base_url: str | None = None,
    ) -> None:
        self._transport = AsyncTransport(token=token or "", base_url=base_url)

    # -- async context-manager support ---------------------------------------

    async def __aenter__(self) -> "AsyncClient":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close()

    async def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        await self._transport.close()

    # -- API methods ---------------------------------------------------------

    async def account_info(self) -> Account:
        data = await self._transport.request("account-info")
        return parse_account(data)

    async def operation_history(
        self,
        type: str | None = None,
        label: str | None = None,
        from_date: datetime | None = None,
        till_date: datetime | None = None,
        start_record: str | None = None,
        records: int | None = None,
        details: bool | None = None,
    ) -> History:
        payload = build_history_payload(
            type=type,
            label=label,
            from_date=from_date,
            till_date=till_date,
            start_record=start_record,
            records=records,
            details=details,
        )
        data = await self._transport.request("operation-history", data=payload)
        return parse_history(data)

    async def operation_details(self, operation_id: str) -> OperationDetails:
        data = await self._transport.request(
            "operation-details",
            data={"operation_id": operation_id},
        )
        return parse_operation_details(data)
