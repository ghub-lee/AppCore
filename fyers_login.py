from fyers_apiv3 import fyersModel
import json
import requests
import pyotp
from urllib import parse
import sys
import json


# Client Info (ENTER YOUR OWN INFO HERE!! Data varies from users and app types)

FY_ID = ""
APP_ID_TYPE = ""
TOTP_KEY = ""
PIN = ""
APP_ID = ""
REDIRECT_URI = ""
APP_TYPE = ""
APP_ID_HASH = ""

# API endpoints
BASE_URL = "https://api-t2.fyers.in/vagator/v2"
BASE_URL_2 = "https://api-t1.fyers.in/api/v3"
URL_SEND_LOGIN_OTP = BASE_URL + "/send_login_otp"
URL_VERIFY_TOTP = BASE_URL + "/verify_otp"
URL_VERIFY_PIN = BASE_URL + "/verify_pin"
URL_TOKEN = BASE_URL_2 + "/token"
URL_VALIDATE_AUTH_CODE = BASE_URL_2 + "/validate-authcode"

SUCCESS = 1
ERROR = -1


class FyeresLogin:

    def send_login_otp(self, fy_id, app_id):
        try:
            payload = {
                "fy_id": fy_id,
                "app_id": app_id
            }
            result_string = requests.post(url=URL_SEND_LOGIN_OTP, json=payload)
            if result_string.status_code != 200:
                return [ERROR, result_string.text]

            result = json.loads(result_string.text)
            request_key = result["request_key"]

            return [SUCCESS, request_key]

        except Exception as e:
            return [ERROR, e]

    def generate_totp(self, secret):
        try:
            generated_totp = pyotp.TOTP(secret).now()
            return [SUCCESS, generated_totp]

        except Exception as e:
            return [ERROR, e]

    def verify_totp(self, request_key, totp):
        try:
            payload = {
                "request_key": request_key,
                "otp": totp
            }
            result_string = requests.post(url=URL_VERIFY_TOTP, json=payload)
            if result_string.status_code != 200:
                return [ERROR, result_string.text]

            result = json.loads(result_string.text)
            request_key = result["request_key"]

            return [SUCCESS, request_key]

        except Exception as e:
            return [ERROR, e]

    def verify_PIN(self, request_key, pin):
        try:
            payload = {
                "request_key": request_key,
                "identity_type": "pin",
                "identifier": pin
            }
            result_string = requests.post(url=URL_VERIFY_PIN, json=payload)
            if result_string.status_code != 200:
                return [ERROR, result_string.text]

            result = json.loads(result_string.text)
            access_token = result["data"]["access_token"]

            return [SUCCESS, access_token]

        except Exception as e:
            return [ERROR, e]

    def token(self, fy_id, app_id, redirect_uri, app_type, access_token):
        try:
            payload = {
                "fyers_id": fy_id,
                "app_id": app_id,
                "redirect_uri": redirect_uri,
                "appType": app_type,
                "code_challenge": "",
                "state": "sample_state",
                "scope": "",
                "nonce": "",
                "response_type": "code",
                "create_cookie": True
            }
            headers = {'Authorization': f'Bearer {access_token}'}

            result_string = requests.post(
                url=URL_TOKEN, json=payload, headers=headers
            )

            if result_string.status_code != 308:
                return [ERROR, result_string.text]

            result = json.loads(result_string.text)
            url = result["Url"]
            auth_code = parse.parse_qs(parse.urlparse(url).query)['auth_code'][0]

            return [SUCCESS, auth_code]

        except Exception as e:
            return [ERROR, e]

    def validate_authcode(self, app_id_hash, auth_code):
        try:
            payload = {
                "grant_type": "authorization_code",
                "appIdHash": app_id_hash,
                "code": auth_code,
            }
            result_string = requests.post(url=URL_VALIDATE_AUTH_CODE, json=payload)
            if result_string.status_code != 200:
                return [ERROR, result_string.text]

            result = json.loads(result_string.text)
            access_token = result["access_token"]

            return [SUCCESS, access_token]

        except Exception as e:
            return [ERROR, e]

    def __init__(self):
        # step 0 Get credential from json file
        # Specify the path to the JSON file
        json_file_path = '../cred.json'

        # Open the JSON file and load its contents into a Python dictionary
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
            FY_ID = data['FY_ID']
            APP_ID_TYPE = data['APP_ID_TYPE']
            TOTP_KEY = data['TOTP_KEY']
            PIN = data['PIN']
            APP_ID = data['APP_ID']
            REDIRECT_URI = data['REDIRECT_URI']
            APP_TYPE = data['APP_TYPE']
            APP_ID_HASH = data['APP_ID_HASH']
    def get_session(self):
        return self.fyers

    def login(self):
        # Step 1 - Retrieve request_key from send_login_otp API
        send_otp_result = self.send_login_otp(fy_id=FY_ID, app_id=APP_ID_TYPE)
        if send_otp_result[0] != SUCCESS:
            print(f"send_login_otp failure - {send_otp_result[1]}")
            sys.exit()
        else:
            print("send_login_otp success")

        # Step 2 - Generate totp
        generate_totp_result = self.generate_totp(secret=TOTP_KEY)
        if generate_totp_result[0] != SUCCESS:
            print(f"generate_totp failure - {generate_totp_result[1]}")
            sys.exit()
        else:
            print("generate_totp success")

        # Step 3 - Verify totp and get request key from verify_otp API
        request_key = send_otp_result[1]
        totp = generate_totp_result[1]
        verify_totp_result = self.verify_totp(request_key=request_key, totp=totp)
        if verify_totp_result[0] != SUCCESS:
            print(f"verify_totp_result failure - {verify_totp_result[1]}")
            sys.exit()
        else:
            print("verify_totp_result success")

        # Step 4 - Verify pin and send back access token
        request_key_2 = verify_totp_result[1]
        verify_pin_result = self.verify_PIN(request_key=request_key_2, pin=PIN)
        if verify_pin_result[0] != SUCCESS:
            print(f"verify_pin_result failure - {verify_pin_result[1]}")
            sys.exit()
        else:
            print("verify_pin_result success")

        # Step 5 - Get auth code for API V2 App from trade access token
        token_result = self.token(
            fy_id=FY_ID, app_id=APP_ID, redirect_uri=REDIRECT_URI, app_type=APP_TYPE,
            access_token=verify_pin_result[1]
        )
        if token_result[0] != SUCCESS:
            print(f"token_result failure - {token_result[1]}")
            sys.exit()
        else:
            print("token_result success")

        # Step 6 - Get API V2 access token from validating auth code
        auth_code = token_result[1]
        validate_authcode_result = self.validate_authcode(
            app_id_hash=APP_ID_HASH, auth_code=auth_code
        )
        if token_result[0] != SUCCESS:
            print(f"validate_authcode failure - {validate_authcode_result[1]}")
            sys.exit()
        else:
            print("validate_authcode success")
        access_token_only = validate_authcode_result[1]
        client_id = APP_ID + "-" + APP_TYPE
        self.fyers = fyersModel.FyersModel(token=access_token_only, is_async=False, client_id=client_id)
        return self.fyers