from AppCore import fyers_login


class Profile:
    fyers_instance = None

    def __init__(self):
        self.fyers_instance = fyers_login.FyeresLogin().login()

    def get_balance(self):
        self.fyers_instance.holdings()




