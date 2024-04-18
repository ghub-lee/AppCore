from AppCore import fyers_login
from AppCore import quotes_handler
from AppCore import data_handler
from AppCore import screener
import threading
import datetime as datetime


# fyers_instance = fyers_login.FyeresLogin()
# session, access_token = fyers_instance.login()
quote_handler_instance = quotes_handler.QuotesHandler()
data_handler_instance = data_handler.DataHandler()
# screener_instance = screener.Screener()


def update_bhav_market_info_copies():
    print('updating bhav files')
    quote_handler_instance.get_BHAV_copy_WithDelivery(datetime.date(2024, 3, 8))
    quote_handler_instance.get_BHAV_copy(datetime.date(2024, 3, 8))
    # quote_handler_instance.get_market_watch()
    # quote_handler_instance.get_block_bulk_deal_data()
    # quote_handler_instance.get_index_quotes_list(index='NIFTY 250', from_web=False)
    # quote_handler_instance.get_index_quotes_list(index='NIFTY 500', from_web=False)


def update_historical_data():

    selected_list = quote_handler_instance.get_index_quotes_list()
    for short_name in selected_list:
        print(short_name)
        data_handler_instance.get_historical_data(short_name)


if __name__ == "__main__":

    # update_bhav_market_info_copies()
    update_historical_data()
    selected_list = quote_handler_instance.get_index_quotes_list()
    # for short_name in selected_list:
    #     thread = threading.Thread(target=data_handler_instance.convert_timeframe(short_name,'1m','15m'))
    #     thread.start()







