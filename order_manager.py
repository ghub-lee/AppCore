import random


class Order:

    def __init__(self):
        self.quantity = 0
        self.buy_price = 0.0
        self.sell_price = 0.0
        self.order_id = 0
        self.script_name = ''


class OrderManager:
    _instance = None
    _orders_list = {}
    wallet_balance = 100000.00
    profitable_trades = 0
    loss_trades = 0

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if not self.initialized:
            self.took_position = False
            self.initialized = True

    def place_order(self, quote_name, buy_price, quantity):
        order = Order()
        order.order_id = self.generate_random_order_id()
        order.buy_price = buy_price
        order.quantity = quantity
        order.script_name = quote_name
        self._orders_list[quote_name] = order
        self.took_position = True
        self.wallet_balance = self.wallet_balance - quantity*buy_price
        print("Placed Order id  Wallet", order.order_id, self.wallet_balance)
        return order.order_id

    def generate_random_order_id(self):
        # Generate a random four-digit number
        four_digit_number = random.randint(1000, 9999)
        return four_digit_number

    def cancel_order(self, order_id):
        pass

    def close_order(self, quote_name, order_id, close_price):
        order = self._orders_list[quote_name]
        self.wallet_balance = self.wallet_balance + order.quantity*close_price
        profit =  order.quantity*(close_price - order.buy_price)
        self.took_position = False
        if order.buy_price > close_price:
            self.loss_trades += 1
            print("Closed::: Order_id,Loss, Bal, Ptrades, LTrades", order_id, profit,self.wallet_balance,
                  self.profitable_trades,self.loss_trades)
        if order.buy_price < close_price:
            self.profitable_trades += 1
            print("Closed::: Order_id,Profit, Bal, Ptrades, LTrades", order_id, profit,self.wallet_balance,
                  self.profitable_trades,self.loss_trades)

    def get_pnl(self, order_id):
        pass


    def get_balance(self):
        return self.wallet_balance

    def get_tradable_balance(self):
        return self.wallet_balance*0.02

