from pydantic import BaseModel, Field

from yoomoney.operation_details.digital_bonus import DigitalBonus
from yoomoney.operation_details.digital_product import DigitalProduct


class DigitalGood(BaseModel):
    products: list[DigitalProduct] = Field(default_factory=list, alias="article")
    bonuses: list[DigitalBonus] = Field(default_factory=list, alias="bonus")

    model_config = {"populate_by_name": True}
