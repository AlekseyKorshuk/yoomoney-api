"""Payment checker with polling loop and label-based verification."""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import Callable, Coroutine
from datetime import datetime, timezone
from typing import Any

from yoomoney.client import Client
from yoomoney.operation.operation import Operation

logger = logging.getLogger(__name__)

SyncCallback = Callable[[Operation], None]
AsyncCallback = Callable[[Operation], Coroutine[Any, Any, None]]


class PaymentChecker:
    """Poll YooMoney operation history and fire callbacks when a payment arrives.

    Typical usage (synchronous)::

        def on_paid(op: Operation) -> None:
            print(f"Received {op.amount} ₽, label={op.label}")

        checker = PaymentChecker(token="TOKEN", interval=5)
        checker.watch(label="order_42", amount=500.0, callback=on_paid, timeout=300)

    Typical usage (asynchronous)::

        async def on_paid(op: Operation) -> None:
            await save_to_db(op)

        checker = PaymentChecker(token="TOKEN", interval=5)
        await checker.watch_async(label="order_42", amount=500.0, callback=on_paid)
    """

    def __init__(self, token: str, interval: float = 10.0) -> None:
        """
        Parameters
        ----------
        token:
            YooMoney OAuth token.
        interval:
            Polling interval in seconds (default 10).
        """
        self._client = Client(token=token)
        self.interval = interval

    def check_label(self, label: str, amount: float | None = None) -> Operation | None:
        """Return the first *incoming* operation matching *label* (and optionally *amount*).

        Returns ``None`` if no matching operation is found.
        """
        history = self._client.operation_history(label=label, type="deposition")
        for op in history.operations:
            if op.label == label and op.status == "success":
                if amount is None or (op.amount is not None and op.amount >= amount):
                    return op
        return None

    def watch(
        self,
        label: str,
        callback: SyncCallback,
        amount: float | None = None,
        timeout: float | None = None,
    ) -> bool:
        """Block until a payment with *label* arrives, then call *callback*.

        Parameters
        ----------
        label:
            Unique label to watch for.
        callback:
            Called with the matching :class:`~yoomoney.operation.operation.Operation`.
        amount:
            Minimum expected amount. Pass ``None`` to accept any amount.
        timeout:
            Stop watching after this many seconds. ``None`` means wait forever.

        Returns
        -------
        bool
            ``True`` if payment was found, ``False`` if timed out.
        """
        deadline = (time.monotonic() + timeout) if timeout is not None else None
        logger.info("Watching for payment: label=%r, amount=%s", label, amount)

        while True:
            op = self.check_label(label, amount)
            if op is not None:
                logger.info("Payment found: operation_id=%s", op.operation_id)
                callback(op)
                return True

            if deadline is not None and time.monotonic() >= deadline:
                logger.warning("Timeout waiting for payment: label=%r", label)
                return False

            time.sleep(self.interval)

    async def check_label_async(self, label: str, amount: float | None = None) -> Operation | None:
        """Async version of :meth:`check_label`."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: self.check_label(label, amount))

    async def watch_async(
        self,
        label: str,
        callback: AsyncCallback,
        amount: float | None = None,
        timeout: float | None = None,
    ) -> bool:
        """Async version of :meth:`watch`.

        The *callback* must be a coroutine function (``async def``).
        """
        start = asyncio.get_event_loop().time()
        logger.info("Async watching for payment: label=%r, amount=%s", label, amount)

        while True:
            op = await self.check_label_async(label, amount)
            if op is not None:
                logger.info("Payment found: operation_id=%s", op.operation_id)
                await callback(op)
                return True

            if timeout is not None and (asyncio.get_event_loop().time() - start) >= timeout:
                logger.warning("Timeout waiting for payment: label=%r", label)
                return False

            await asyncio.sleep(self.interval)

    @staticmethod
    def make_label(prefix: str = "order") -> str:
        """Generate a unique label based on *prefix* and current UTC timestamp.

        Example: ``"order_1718000000123456"``
        """
        ts = int(datetime.now(tz=timezone.utc).timestamp() * 1_000_000)
        return f"{prefix}_{ts}"
