

class BalanceDetails:
    def __init__(self,
                 total: float = None,
                 available: float = None,
                 deposition_pending: float = None,
                 blocked: float = None,
                 debt: float = None,
                 hold: float = None,
                 ):

        self.total = total

        self.available = available

        self.deposition_pending = deposition_pending

        self.blocked = blocked

        self.debt = debt

        self.hold = hold




