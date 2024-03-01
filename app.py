from AppCore import fyers_login
from AppCore import quotes_handler
from AppCore import data_handler
from AppCore import screener
from datetime import datetime

# Initialize the start date
# Example: January 1, 2022
start_date_out = datetime(2024, 2, 1)
# Specify the end date
end_date_out = datetime.now()


if __name__ == "__main__":
    # pass

    # fyers_instance = fyers_login.FyeresLogin()
    # session = fyers_instance.login()

    quote_handler_instance = quotes_handler.QuotesHandler()
    data_handler_instance = data_handler.DataHandler()
    # quote_handler_instance.get_BHAV_copy_WithDelivery(datetime.now())
    # quote_handler_instance.get_BHAV_copy(datetime.now())
    # quote_handler_instance.get_market_watch()
    # list = quote_handler_instance.get_advance_decline_index_list(percentage=80)
    # list = quote_handler_instance.get_quotes_list()
    # quote_handler_instance.save_selected_quotes_to_excel(list)
    # list = quote_handler_instance.get_index_quotes_list(index='NIFTY 250', from_web=False)
    # quote_handler_instance.get_sectoral_quote_information('NIFTY HEALTHCARE')



    # screener_instance = screener.Screener()
    # screener_instance.get_stock_price_ranged_previous_day(120,20)

    selected_list = quote_handler_instance.get_index_quotes_list()
    for index, short_name in enumerate(selected_list):
        data_handler_instance.get_historical_data(short_name, start_date=start_date_out, end_date=end_date_out)





