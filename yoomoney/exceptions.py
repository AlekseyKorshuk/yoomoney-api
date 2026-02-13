from typing import Any


class YooMoneyError(Exception):
    """Base class for all YooMoney API errors."""

    message: str = "Unknown error"

    def __init__(self) -> None:
        super().__init__(self.message)


# -- Authentication / authorisation errors ----------------------------------


class InvalidToken(YooMoneyError):
    message = "Token is not valid, or does not have the appropriate rights"


class EmptyToken(YooMoneyError):
    message = "Response token is empty. Repeated request for an authorization token"


class InvalidRequest(YooMoneyError):
    message = "Required query parameters are missing or have incorrect or invalid values"


class UnauthorizedClient(YooMoneyError):
    message = (
        "Invalid parameter value 'client_id' or 'client_secret', or the application"
        " does not have the right to request authorization"
        " (for example, YooMoney blocked it 'client_id')"
    )


class InvalidGrant(YooMoneyError):
    message = (
        "In issue 'access_token' denied. YuMoney did not issue a temporary token, "
        "the token is expired, or this temporary token has already been issued "
        "'access_token' (repeated request for an authorization token with the same temporary token)"
    )


# -- Illegal parameter errors -----------------------------------------------


class IllegalParamType(YooMoneyError):
    message = "Invalid parameter value 'type'"


class IllegalParamStartRecord(YooMoneyError):
    message = "Invalid parameter value 'start_record'"


class IllegalParamRecords(YooMoneyError):
    message = "Invalid parameter value 'records'"


class IllegalParamLabel(YooMoneyError):
    message = "Invalid parameter value 'label'"


class IllegalParamFromDate(YooMoneyError):
    message = "Invalid parameter value 'from_date'"


class IllegalParamTillDate(YooMoneyError):
    message = "Invalid parameter value 'till_date'"


class IllegalParamOperationId(YooMoneyError):
    message = "Invalid parameter value 'operation_id'"


# -- Technical errors --------------------------------------------------------


class TechnicalError(YooMoneyError):
    message = "Technical error, try calling the operation again later"


# -- Error mapping -----------------------------------------------------------

ERROR_MAP: dict[str, type[YooMoneyError]] = {
    "illegal_param_type": IllegalParamType,
    "illegal_param_start_record": IllegalParamStartRecord,
    "illegal_param_records": IllegalParamRecords,
    "illegal_param_label": IllegalParamLabel,
    "illegal_param_from": IllegalParamFromDate,
    "illegal_param_till": IllegalParamTillDate,
    "illegal_param_operation_id": IllegalParamOperationId,
    "invalid_request": InvalidRequest,
    "unauthorized_client": UnauthorizedClient,
    "invalid_grant": InvalidGrant,
}


def raise_for_error(data: dict[str, Any]) -> None:
    """Raise the appropriate exception if *data* contains an ``error`` key."""
    if "error" in data:
        exc_class = ERROR_MAP.get(data["error"], TechnicalError)
        raise exc_class()
