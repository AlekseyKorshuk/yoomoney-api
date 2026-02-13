from pydantic import BaseModel


class BalanceDetails(BaseModel):
    total: float | None = None
    available: float | None = None
    deposition_pending: float | None = None
    blocked: float | None = None
    debt: float | None = None
    hold: float | None = None
