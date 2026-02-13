from pydantic import BaseModel, Field

from yoomoney.account.balance_details import BalanceDetails
from yoomoney.account.card import Card


class Account(BaseModel):
    account: str
    balance: float
    currency: str
    account_status: str
    account_type: str
    balance_details: BalanceDetails | None = None
    cards_linked: list[Card] = Field(default_factory=list)
