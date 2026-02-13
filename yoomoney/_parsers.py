"""Response-parsing helpers for the YooMoney API.

Each ``parse_*`` function validates the raw JSON dict returned by the API,
raises the appropriate exception on error, and returns a typed Pydantic model.
"""

from datetime import datetime
from typing import Any

from yoomoney.account.account import Account
from yoomoney.exceptions import InvalidToken, raise_for_error
from yoomoney.history.history import History
from yoomoney.operation_details.operation_details import OperationDetails


def parse_account(data: dict[str, Any]) -> Account:
    """Parse an ``account-info`` API response into an :class:`Account`."""
    if not data:
        raise InvalidToken()
    return Account.model_validate(data)


def parse_history(data: dict[str, Any]) -> History:
    """Parse an ``operation-history`` API response into a :class:`History`."""
    raise_for_error(data)
    return History.model_validate(data)


def parse_operation_details(data: dict[str, Any]) -> OperationDetails:
    """Parse an ``operation-details`` API response into :class:`OperationDetails`."""
    raise_for_error(data)
    return OperationDetails.model_validate(data)


def format_datetime(value: datetime | None) -> str | None:
    """Format a *datetime* for use in API request payloads."""
    if value is None:
        return None
    return f"{value.year}-{value.month}-{value.day}T{value.hour}:{value.minute}:{value.second}"


def build_history_payload(
    type: str | None = None,
    label: str | None = None,
    from_date: datetime | None = None,
    till_date: datetime | None = None,
    start_record: str | None = None,
    records: int | None = None,
    details: bool | None = None,
) -> dict[str, Any]:
    """Build the form-data payload for an ``operation-history`` request."""
    payload: dict[str, Any] = {}
    if type is not None:
        payload["type"] = type
    if label is not None:
        payload["label"] = label
    if from_date is not None:
        payload["from"] = format_datetime(from_date)
    if till_date is not None:
        payload["till"] = format_datetime(till_date)
    if start_record is not None:
        payload["start_record"] = start_record
    if records is not None:
        payload["records"] = records
    if details is not None:
        payload["details"] = details
    return payload
