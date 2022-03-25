from datetime import datetime
from typing import Optional
import requests
import json



class RequestPayment:
    def __init__(self,
                 base_url: str = None,
                 token: str = None,
                 method: str = None,
                 pattern_id: str = "p2p",
                 to: str = None,
                 amount: float = None,
                 amount_due: float = None,
                 comment: str = None,
                 message: str = None,
                 label: str = None,
                 codepro: bool = True,
                 expire_period: int = 1,
                 ):

        self.__private_method = method

        self.__private_base_url = base_url
        self.__private_token = token

        self.label = label
        self.pattern_id = pattern_id
        self.to = to
        self.amount = amount
        self.amount_due = amount_due
        self.comment = comment
        self.message = message
        self.codepro = codepro
        self.expire_period = expire_period

        self.result = self._request()
        self.__dict__ = {**self.__dict__, **self.result}

    def __getattr__(self, attr):
        return self[attr]

    def _request(self):

        access_token = str(self.__private_token)
        url = self.__private_base_url + self.__private_method

        headers = {
            'Authorization': 'Bearer ' + str(access_token),
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        payload = {}
        if self.pattern_id is not None:
            payload["pattern_id"] = self.pattern_id
        if self.label is not None:
            payload["label"] = self.label
        if self.to is not None:
            payload["to"] = self.to
        if self.amount is not None:
            payload["amount"] = self.amount
        if self.amount_due is not None:
            payload["amount_due"] = self.amount_due
        if self.comment is not None:
            payload["comment"] = self.comment
        if self.message is not None:
            payload["message"] = self.message
        if self.codepro is not None:
            payload["codepro"] = self.codepro
        if self.codepro is not None:
            payload["expire_period"] = self.expire_period

        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()
