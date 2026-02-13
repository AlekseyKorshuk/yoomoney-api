from datetime import datetime as dt

from pydantic import BaseModel, field_validator

from yoomoney.operation_details.digital_good import DigitalGood


class OperationDetails(BaseModel):
    operation_id: str | None = None
    status: str | None = None
    pattern_id: str | None = None
    direction: str | None = None
    amount: float | None = None
    amount_due: float | None = None
    fee: float | None = None
    datetime: dt | None = None
    title: str | None = None
    sender: str | None = None
    recipient: str | None = None
    recipient_type: str | None = None
    message: str | None = None
    comment: str | None = None
    codepro: bool | None = None
    protection_code: str | None = None
    expires: dt | None = None
    answer_datetime: dt | None = None
    label: str | None = None
    details: str | None = None
    type: str | None = None
    digital_goods: DigitalGood | None = None

    @field_validator("datetime", "expires", "answer_datetime", mode="before")
    @classmethod
    def _parse_datetime(cls, v: object) -> object:
        if isinstance(v, str):
            return dt.fromisoformat(v.replace("Z", ""))
        return v
