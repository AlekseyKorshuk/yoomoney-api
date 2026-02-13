from pydantic import BaseModel, Field

from yoomoney.operation.operation import Operation


class History(BaseModel):
    next_record: str | None = None
    operations: list[Operation] = Field(default_factory=list)
