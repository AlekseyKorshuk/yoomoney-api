from datetime import datetime as dt

from pydantic import BaseModel, field_validator


class Operation(BaseModel):
    operation_id: str | None = None
    status: str | None = None
    datetime: dt | None = None
    title: str | None = None
    pattern_id: str | None = None
    direction: str | None = None
    amount: float | None = None
    label: str | None = None
    type: str | None = None

    @field_validator("datetime", mode="before")
    @classmethod
    def _parse_datetime(cls, v: object) -> object:
        if isinstance(v, str):
            return dt.fromisoformat(v.replace("Z", ""))
        return v
