

class YooMoneyError(Exception):
    """Basic class"""


class InvalidToken(YooMoneyError):

    message = "Token is not valid, or does not have the appropriate rights"
    def __init__(self, ):
        super().__init__(self.message)


class IllegalParamType(YooMoneyError):

    message = "Invalid parameter value 'type'"
    def __init__(self, ):
        super().__init__(self.message)

class IllegalParamStartRecord(YooMoneyError):

    message = "Invalid parameter value 'start_record'"
    def __init__(self, ):
        super().__init__(self.message)


class IllegalParamRecords(YooMoneyError):

    message = "Invalid parameter value 'records'"
    def __init__(self, ):
        super().__init__(self.message)

class IllegalParamLabel(YooMoneyError):

    message = "Invalid parameter value 'label'"
    def __init__(self, ):
        super().__init__(self.message)

class IllegalParamFromDate(YooMoneyError):

    message = "Invalid parameter value 'from_date'"
    def __init__(self, ):
        super().__init__(self.message)


class IllegalParamTillDate(YooMoneyError):

    message = "Invalid parameter value 'till_date'"
    def __init__(self, ):
        super().__init__(self.message)

class IllegalParamOperationId(YooMoneyError):

    message = "Invalid parameter value 'operation_id'"
    def __init__(self, ):
        super().__init__(self.message)

class TechnicalError(YooMoneyError):

    message = "Technical error, try calling the operation again later"
    def __init__(self, ):
        super().__init__(self.message)

class InvalidRequest(YooMoneyError):

    message = "Required query parameters are missing or have incorrect or invalid values"
    def __init__(self, ):
        super().__init__(self.message)

class UnauthorizedClient(YooMoneyError):

    message = "Invalid parameter value 'client_id' or 'client_secret', or the application" \
              " does not have the right to request authorization (for example, YooMoney blocked it 'client_id')"
    def __init__(self, ):
        super().__init__(self.message)

class InvalidGrant(YooMoneyError):

    message = "In issue 'access_token' denied. YuMoney did not issue a temporary token, " \
              "the token is expired, or this temporary token has already been issued " \
              "'access_token' (repeated request for an authorization token with the same temporary token)"
    def __init__(self, ):
        super().__init__(self.message)

class EmptyToken(YooMoneyError):

    message = "Response token is empty. Repeated request for an authorization token"
    def __init__(self, ):
        super().__init__(self.message)