"""Webhook helpers for YooMoney payment notifications."""

from __future__ import annotations

import hashlib
import inspect
import logging
from collections.abc import Callable
from typing import Any

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class Notification(BaseModel):
    """Parsed YooMoney HTTP-notification payload.

    Reference: https://yoomoney.ru/docs/payment-buttons/using-api/notifications
    """

    notification_type: str
    operation_id: str
    amount: float
    currency: str = "643"
    datetime: str
    sender: str = ""
    codepro: bool = False
    label: str = ""
    sha1_hash: str = Field(alias="sha1_hash", default="")

    model_config = {"populate_by_name": True}

    def verify_signature(self, secret: str) -> bool:
        """Return ``True`` if the SHA-1 signature matches *secret*."""
        codepro_str = "true" if self.codepro else "false"
        raw = "&".join(
            [
                self.notification_type,
                self.operation_id,
                str(self.amount),
                self.currency,
                self.datetime,
                self.sender,
                codepro_str,
                secret,
                self.label,
            ]
        )
        expected = hashlib.sha1(raw.encode()).hexdigest()  # noqa: S324
        return expected == self.sha1_hash


async def fastapi_webhook(
    request: Any,
    secret: str,
    on_payment: Callable[[Notification], Any],
    *,
    verify: bool = True,
) -> Any:
    """Handle a YooMoney notification inside a FastAPI route.

    Parameters
    ----------
    request:
        The ``fastapi.Request`` object from your route handler.
    secret:
        The notification secret from your YooMoney settings.
    on_payment:
        Callable (sync or async) invoked with :class:`Notification`.
    verify:
        If ``True`` (default), reject notifications with invalid signatures.
    """
    try:
        from fastapi.responses import PlainTextResponse  # type: ignore[import-untyped]
    except ImportError as exc:
        msg = "FastAPI is not installed. Run: pip install fastapi python-multipart"
        raise ImportError(msg) from exc

    form = await request.form()
    form_dict: dict[str, Any] = dict(form)
    notification = Notification.model_validate(form_dict)

    if verify and not notification.verify_signature(secret):
        logger.warning("Invalid YooMoney signature")
        return PlainTextResponse("Bad signature", status_code=400)

    logger.info(
        "YooMoney payment: operation_id=%s, amount=%s, label=%r",
        notification.operation_id,
        notification.amount,
        notification.label,
    )

    result = on_payment(notification)
    if inspect.isawaitable(result):
        await result

    return PlainTextResponse("OK", status_code=200)
