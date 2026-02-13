from typing import Any

import httpx


class Quickpay:
    """Build and execute a YooMoney QuickPay payment form."""

    _BASE = "https://yoomoney.ru/quickpay/confirm.xml"

    def __init__(
        self,
        receiver: str,
        quickpay_form: str,
        targets: str,
        paymentType: str,
        sum: float,
        formcomment: str | None = None,
        short_dest: str | None = None,
        label: str | None = None,
        comment: str | None = None,
        successURL: str | None = None,
        need_fio: bool | None = None,
        need_email: bool | None = None,
        need_phone: bool | None = None,
        need_address: bool | None = None,
    ) -> None:
        self.receiver = receiver
        self.quickpay_form = quickpay_form
        self.targets = targets
        self.paymentType = paymentType
        self.sum = sum
        self.formcomment = formcomment
        self.short_dest = short_dest
        self.label = label
        self.comment = comment
        self.successURL = successURL
        self.need_fio = need_fio
        self.need_email = need_email
        self.need_phone = need_phone
        self.need_address = need_address

        self.response = self._request()

    # -- internals -----------------------------------------------------------

    def _build_params(self) -> dict[str, Any]:
        """Build URL query parameters, using the hyphenated keys the API expects."""
        mapping: dict[str, Any] = {
            "receiver": self.receiver,
            "quickpay-form": self.quickpay_form,
            "targets": self.targets,
            "paymentType": self.paymentType,
            "sum": self.sum,
            "formcomment": self.formcomment,
            "short-dest": self.short_dest,
            "label": self.label,
            "comment": self.comment,
            "successURL": self.successURL,
            "need-fio": self.need_fio,
            "need-email": self.need_email,
            "need-phone": self.need_phone,
            "need-address": self.need_address,
        }
        return {k: v for k, v in mapping.items() if v is not None}

    def _request(self) -> httpx.Response:
        params = self._build_params()
        # Build the full URL with properly-encoded query string
        request = httpx.Request("GET", self._BASE, params=params)
        self.base_url = str(request.url)

        response = httpx.post(self.base_url, follow_redirects=True)
        self.redirected_url = str(response.url)
        return response
