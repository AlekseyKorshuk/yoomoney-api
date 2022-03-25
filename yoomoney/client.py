import requests
import json
from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Union
from datetime import datetime

from yoomoney import (
    Account,
    History,
    OperationDetails,
    RequestPayment,
)


class Client:
    def __init__(self,
                 token: str = None,
                 base_url: str = None,
                 ):

        if base_url is None:
            self.base_url = "https://yoomoney.ru/api/"

        if token is not None:
            self.token = token

    def account_info(self):
        method = "account-info"
        return Account(base_url=self.base_url,
                       token=self.token,
                       method=method
                       )

    def operation_history(self,
                          type: str = None,
                          label: str = None,
                          from_date: datetime = None,
                          till_date: datetime = None,
                          start_record: str = None,
                          records: int = None,
                          details: bool = None,
                          ):
        method = "operation-history"
        return History(base_url=self.base_url,
                       token=self.token,
                       method=method,
                       type=type,
                       label=label,
                       from_date=from_date,
                       till_date=till_date,
                       start_record=start_record,
                       records=records,
                       details=details,
                       )

    def operation_details(self,
                          operation_id: str
                          ):
        method = "operation-details"
        return OperationDetails(base_url=self.base_url,
                                token=self.token,
                                method=method,
                                operation_id=operation_id,
                                )

    def request_payment(self,
                        pattern_id: str = "p2p",
                        to: str = "410019014512803",
                        amount: float = None,
                        amount_due: float = None,
                        comment: str = None,
                        message: str = None,
                        label: str = None,
                        codepro: bool = True,
                        expire_period: int = 1,
                        ):
        method = "request-payment"
        return RequestPayment(base_url=self.base_url,
                              token=self.token,
                              method=method,
                              pattern_id=pattern_id,
                              to=to,
                              amount=amount,
                              amount_due=amount_due,
                              comment=comment,
                              message=message,
                              label=label,
                              codepro=codepro,
                              expire_period=expire_period,
                              )
