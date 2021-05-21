from typing import List
import requests

from yoomoney.exceptions import (
    InvalidRequest,
    UnauthorizedClient,
    InvalidGrant,
    EmptyToken
    )

class Authorize:
    def __init__(
            self,
            client_id: str,
            redirect_uri: str,
            scope: List[str]
                  ):

        url = "https://yoomoney.ru/oauth/authorize?client_id={client_id}&response_type=code" \
              "&redirect_uri={redirect_uri}&scope={scope}".format(client_id=client_id,
                                                                  redirect_uri=redirect_uri,
                                                                  scope='%20'.join([str(elem) for elem in scope]),
                                                                  )

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers)

        if response.status_code == 200:
            print("Visit this website and confirm the application authorization request:")
            print(response.url)

        code = str(input("Enter redirected url (https://yourredirect_uri?code=XXXXXXXXXXXXX) or just code: "))
        try:
            code = code[code.index("code=") + 5:].replace(" ","")
        except:
            pass

        url = "https://yoomoney.ru/oauth/token?code={code}&client_id={client_id}&" \
              "grant_type=authorization_code&redirect_uri={redirect_uri}".format(code=str(code),
                                                                                 client_id=client_id,
                                                                                 redirect_uri=redirect_uri,
                                                                                 )

        response = requests.request("POST", url, headers=headers)

        if "error" in response.json():
            error = response.json()["error"]
            if error == "invalid_request":
                raise InvalidRequest()
            elif error == "unauthorized_client":
                raise UnauthorizedClient()
            elif error == "invalid_grant":
                raise InvalidGrant()

        if response.json()['access_token'] == "":
            raise EmptyToken()

        print("Your access token:")
        print(response.json()['access_token'])