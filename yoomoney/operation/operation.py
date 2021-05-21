from datetime import datetime as dt
from typing import Optional

class Operation:
    def __init__(self,
                 operation_id: str = None,
                 status: str = None,
                 datetime: Optional[dt] = None,
                 title: str = None,
                 pattern_id: str = None,
                 direction: str = None,
                 amount: float = None,
                 label: str = None,
                 type: str = None,
                 ):
        self.operation_id = operation_id
        self.status = status
        self.datetime = datetime
        self.title = title
        self.pattern_id = pattern_id
        self.direction = direction
        self.amount = amount
        self.label = label
        self.type = type