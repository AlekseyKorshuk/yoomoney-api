from datetime import datetime
from typing import Optional, List
import requests

from yoomoney.exceptions import (
    IllegalParamOperationId,
    TechnicalError
    )

from yoomoney.operation_details.digital_product import DigitalProduct
from yoomoney.operation_details.digital_bonus import DigitalBonus
from yoomoney.operation_details.digital_good import DigitalGood


class OperationDetails:
    def __init__(self,
                 base_url: str,
                 token: str,
                 operation_id: str,
                 method: str = None,
                 ):
        self.__private_method = method
        self.__private_token = token
        self.__private_base_url = base_url
        self.operation_id = operation_id

        data = self._request()

        if "error" in data:
            if data["error"] == "illegal_param_operation_id":
                raise IllegalParamOperationId()
            else:
                raise TechnicalError()

        self.status = None
        self.pattern_id = None
        self.direction = None
        self.amount = None
        self.amount_due = None
        self.fee = None
        self.datetime = None
        self.title = None
        self.sender = None
        self.recipient = None
        self.recipient_type = None
        self.message = None
        self.comment = None
        self.codepro = None
        self.protection_code = None
        self.expires = None
        self.answer_datetime = None
        self.label = None
        self.details = None
        self.type = None
        self.digital_goods = None

        if "status" in data:
            self.status = data["status"]
        if "pattern_id" in data:
            self.pattern_id = data["pattern_id"]
        if "direction" in data:
            self.direction = data["direction"]
        if "amount" in data:
            self.amount = data["amount"]
        if "amount_due" in data:
            self.amount_due = data["amount_due"]
        if "fee" in data:
            self.fee = data["fee"]
        if "datetime" in data:
            self.datetime = datetime.strptime(str(data["datetime"]).replace("T", " ").replace("Z", ""), '%Y-%m-%d %H:%M:%S')
        if "title" in data:
            self.title = data["title"]
        if "sender" in data:
            self.sender = data["sender"]
        if "recipient" in data:
            self.recipient = data["recipient"]
        if "recipient_type" in data:
            self.recipient_type = data["recipient_type"]
        if "message" in data:
            self.message = data["message"]
        if "comment" in data:
            self.comment = data["comment"]
        if "codepro" in data:
            self.codepro = bool(data["codepro"])
        if "protection_code" in data:
            self.protection_code = data["protection_code"]
        if "expires" in data:
            self.datetime = datetime.strptime(str(data["expires"]).replace("T", " ").replace("Z", ""), '%Y-%m-%d %H:%M:%S')
        if "answer_datetime" in data:
            self.datetime = datetime.strptime(str(data["answer_datetime"]).replace("T", " ").replace("Z", ""), '%Y-%m-%d %H:%M:%S')
        if "label" in data:
            self.label = data["label"]
        if "details" in data:
            self.details = data["details"]
        if "type" in data:
            self.type = data["type"]
        if "digital_goods" in data:
            products: List[DigitalProduct] = []
            for product in data["digital_goods"]["article"]:
                digital_product = DigitalProduct(merchant_article_id=product["merchantArticleId"],
                                                 serial=product["serial"],
                                                 secret=product["secret"],
                                                 )
                products.append(digital_product)

            bonuses: List[DigitalBonus] = []
            for bonus in data["digital_goods"]["bonus"]:
                digital_product = DigitalBonus(serial=bonus["serial"],
                                               secret=bonus["secret"],
                                               )
                bonuses.append(digital_product)

            self.digital_goods = DigitalGood(products=products,
                                             bonuses=bonuses
                                             )

    def _request(self):

        access_token = str(self.__private_token)
        url = self.__private_base_url + self.__private_method

        headers = {
            'Authorization': 'Bearer ' + str(access_token),
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        payload = {}

        payload["operation_id"] = self.operation_id


        response = requests.request("POST", url, headers=headers, data=payload)

        return response.json()
