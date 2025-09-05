from yoomoney.operation_details.digital_product import DigitalProduct
from yoomoney.operation_details.digital_bonus import DigitalBonus

from typing import List


class DigitalGood:
    def __init__(
        self,
        products: List[DigitalProduct],
        bonuses: List[DigitalBonus]
    ):
        
        self.products = products
        self.bonuses = bonuses
