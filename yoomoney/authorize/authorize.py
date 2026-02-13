import httpx

from yoomoney.exceptions import EmptyToken, raise_for_error

_OAUTH_AUTHORIZE_URL = "https://yoomoney.ru/oauth/authorize"
_OAUTH_EXCHANGE_URL = "https://yoomoney.ru/oauth/token"
_HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}


class Authorize:
    """Interactive OAuth2 authorization flow for YooMoney.

    Prints the authorization URL, waits for the user to paste the redirect
    URL (or code), exchanges it for an access token, and prints the result.
    """

    def __init__(
        self,
        client_id: str,
        redirect_uri: str,
        client_secret: str,
        scope: list[str],
    ) -> None:
        # Step 1 -- redirect the user to the consent page
        auth_url = self._build_authorize_url(client_id, redirect_uri, scope)
        response = httpx.post(auth_url, headers=_HEADERS, follow_redirects=True)

        if response.status_code == 200:
            print("Visit this website and confirm the application authorization request:")
            print(str(response.url))

        # Step 2 -- collect the authorization code from the user
        code = self._prompt_for_code()

        # Step 3 -- exchange the code for an access token
        access_token = self._exchange_code(
            code=code,
            client_id=client_id,
            redirect_uri=redirect_uri,
            client_secret=client_secret,
        )

        print("Your access token:")
        print(access_token)

    # -- helpers (static / class methods for testability) --------------------

    @staticmethod
    def _build_authorize_url(client_id: str, redirect_uri: str, scope: list[str]) -> str:
        params = {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "scope": " ".join(scope),
        }
        request = httpx.Request("GET", _OAUTH_AUTHORIZE_URL, params=params)
        return str(request.url)

    @staticmethod
    def _prompt_for_code() -> str:
        raw = input(
            "Enter redirected url (https://yourredirect_uri?code=XXXXXXXXXXXXX) or just code: "
        )
        try:
            return raw[raw.index("code=") + 5 :].strip()
        except ValueError:
            return raw.strip()

    @staticmethod
    def _exchange_code(
        code: str,
        client_id: str,
        redirect_uri: str,
        client_secret: str,
    ) -> str:
        """Exchange an authorization *code* for an access token."""
        payload = {
            "code": code,
            "client_id": client_id,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
            "client_secret": client_secret,
        }
        response = httpx.post(_OAUTH_EXCHANGE_URL, headers=_HEADERS, data=payload)
        data = response.json()

        raise_for_error(data)

        if data.get("access_token", "") == "":
            raise EmptyToken()

        access_token: str = data["access_token"]
        return access_token
