import talib
import numpy as np
import math
import pandas as pd
from order_manager import OrderManager

from data_handler import DataHandler
import threading

data_handler_instance = DataHandler()
order_manager = OrderManager()


class BackTester:

    order_id = 0

    def __init__(self, short_quote_name):
        self.dataframe_15min = data_handler_instance.convert_timeframe(short_quote_name=short_quote_name,
                                                                       intended_timeframe='15m', original_timeframe='1m')
        self.dataframe_1hour = data_handler_instance.convert_timeframe(short_quote_name=short_quote_name,
                                                                       intended_timeframe='1h', original_timeframe='1m')
        self.thread = None
        self.short_quote_name = short_quote_name
        self.create_backtest_thread()
        self.thread.start()
        self.thread.join()

    def create_backtest_thread(self):
        # Create a thread object
        self.thread = threading.Thread(target=self.backtest)

    def get_balance(self):
        return order_manager.get_balance()

    def backtest(self):
        close = []
        for index, row in self.dataframe_1hour.iterrows():
            current_close = row['Close']
            close.append(current_close)
            close_array = np.array(close)
            ema = talib.EMA(close_array, timeperiod=21)
            ema_value = float(ema[-1])
            if ema_value != np.NaN and current_close != np.NaN:
                if ema_value < current_close:
                    self.look_for_buy(row['Date'])
                else:
                    print("Start Sell Thread")

    def look_for_buy(self, timestamp):
        close = []
        # Define the particular timestamp
        start_timestamp = pd.Timestamp(timestamp)
        # Filter DataFrame values after the particular timestamp
        filtered_df = self.dataframe_15min.loc[self.dataframe_15min['Date'] >= start_timestamp]
        for index, row in filtered_df.iterrows():
            current_close = row['Close']
            close.append(current_close)
            close_array = np.array(close)
            ema21 = talib.EMA(close_array, timeperiod=21)
            ema9 = talib.EMA(close_array, timeperiod=9)
            ema21_value = float(ema21[-1])
            ema9_value = float(ema9[-1])

            if ema21_value != np.NaN and ema9_value != np.NaN and current_close != np.NaN:
                if ema9_value > ema21_value:
                    if not order_manager.took_position:
                        try:
                            next_row = self.dataframe_15min.iloc[index + 1]
                            buy_price = float(next_row['Open'])
                            quantity = math.floor(order_manager.get_tradable_balance()/buy_price)
                            self.order_id = order_manager.place_order(quote_name=self.short_quote_name,
                                                                      buy_price=buy_price, quantity=quantity)
                        except StopIteration:
                            print("\nNo more rows after this one")

                else:
                    if order_manager.took_position:
                        try:
                            next_row = self.dataframe_15min.iloc[index + 1]
                            close_price = float(next_row['Open'])
                            order_manager.close_order(quote_name=self.short_quote_name,close_price=close_price,
                                                      order_id=self.order_id)
                        except StopIteration:
                            print("\nNo more rows after this one")


if __name__ == "__main__":

    bt = BackTester('ANURAS')
    # bt2 = BackTester('BCG')
