'''
Its Purpose is to get data
of 1 min resolution.
Input will be symbol name,from date and to date
'''

import nsepy as ns
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import numpy as np
import os
import constants
import csv

format_str = '%Y-%m-%d %H:%M:%S'


class DataHandler:
    def __init__(self):
        pass

    def get_historical_data(self, short_quote_name):

        short_quote_name = short_quote_name.upper()

        excel_file = constants.HISTORICAL_DATA_FILES_DIR_PATH + f'{short_quote_name}.xlsx'

        local_start_date = None
        if os.path.exists(excel_file):
            df = pd.read_excel(excel_file)
            local_start_date = df['Date'].iloc[-1]
            print(f'File exist for {short_quote_name} with date',local_start_date)
        else:
            print('Getting last 30 days data')
            man_start_date = datetime.now()-timedelta(days=29)
            local_start_date = man_start_date

        end_date = datetime.now().date()
        start_date = local_start_date.date()

        new_data_frame = pd.DataFrame(columns=['Date', 'Open', 'High', ' Low', 'Close', 'Volume'])

        while start_date <= end_date:
            temp_date = start_date + timedelta(days=1)
            stock = yf.Ticker(short_quote_name + '.NS')
            df = stock.history(start=start_date, end=temp_date, interval="1m")
            start_date = temp_date
            # For 1h:The requested range must be within the last 730 days.
            # For 15min:The requested range must be within the last 60 days.
            # For 30min:The requested range must be within the last 60 days.
            # For 1m:The requested range must be within the last 30 days.
            data_frame = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
            # df.tz_localize(tz=None, axis=0)
            # data_frame['Date'] = df._axis(0).tz_localize(None)
            # data_frame['Date'] = df['DatetimeIndex'].tz_localize(None)
            data_frame['Date'] = pd.to_datetime(df.index, format=constants.DATE_INDIAN_FORMAT_STRING).tz_localize(None)
            data_frame['Date'] = data_frame['Date'].array
            data_frame['Open'] = df['Open'].array
            data_frame['High'] = df['High'].array
            data_frame['Low'] = df['Low'].array
            data_frame['Close'] = df['Close'].array
            data_frame['Volume'] = df['Volume'].array
            new_data_frame = pd.concat([new_data_frame.reset_index(drop=True), data_frame.reset_index(drop=True)],
                                       verify_integrity=True, ignore_index=True)
        try:
            if not os.path.exists(excel_file):
                new_data_frame.to_excel(excel_file, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'], index=True)
            else:
                with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                    new_data_frame.to_excel(writer, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'],
                                            index=True, header=False, startrow=writer.sheets['Sheet1'].max_row)
        except Exception as e:
            print("exception occur", e)

    def convert_timeframe(self, short_quote_name, original_timeframe, intended_timeframe):

        short_quote_name = short_quote_name.upper()
        original_file = constants.HISTORICAL_DATA_FILES_DIR_PATH + f'{short_quote_name}.xlsx'

        candles_count = self.get_candles_count(original_timeframe, intended_timeframe)

        df = pd.read_excel(original_file, index_col=None)
        dataframe = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
        for index in range(0, df.shape[0], candles_count):
            new_dataframe = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
            subset_df = df.iloc[index:index + candles_count].reset_index(drop=True)  # Select the first four rows
            new_dataframe.loc[0, 'Date'] = subset_df.loc[0, 'Date']
            new_dataframe.loc[0, 'Open'] = subset_df.loc[0, 'Open']
            new_dataframe.loc[0, 'High'] = subset_df['High'].max(axis=0)
            new_dataframe.loc[0, 'Low'] = subset_df['Low'].min(axis=0)
            new_dataframe.loc[0, 'Close'] = subset_df['Close'].iloc[-1]
            new_dataframe.loc[0, 'Volume'] = subset_df['Volume'].sum(axis=0)
            dataframe = pd.concat([dataframe.reset_index(drop=True), new_dataframe.reset_index(drop=True)]
                                           ,verify_integrity=True, ignore_index=True)
        print('**********',short_quote_name)
        print(dataframe.head())
        # return dataframe

    def get_candles_count(self, original_timeframe, intended_timeframe):

        if original_timeframe == '1m':
            if intended_timeframe == '1h':
                return 60
            if intended_timeframe == '15m':
                return 15
            if intended_timeframe == '30m':
                return 30

        if original_timeframe == '15m':
            if intended_timeframe == '1h':
                return 4
            if intended_timeframe == '30m':
                return 3


    def run_strategy(self):
        df = pd.read_excel("./infy.xlsx", index_col=None)
        ltp = 0
        for index in range(0, df.shape[0], 1):
            subset_df = df.iloc[0:index + 1].reset_index(drop=True)
            sma21 = subset_df.Close.rolling(21).mean()
            ltp = subset_df.loc[-1:'Close']
            print(ltp)

    # from datetime import datetime
    #
    # # Time strings
    # time_str1 = '2022-02-20 10:30:00'
    # time_str2 = '2022-02-20 12:00:00'
    #
    # # Parse time strings to datetime objects
    # time1 = datetime.strptime(time_str1, '%Y-%m-%d %H:%M:%S')
    # time2 = datetime.strptime(time_str2, '%Y-%m-%d %H:%M:%S')
    # Formatted timestamp string
    # timestamp_str = '2024-02-20 12:30:45'  # Example timestamp string
    #
    # # Define the format of the timestamp string
    # format_str = '%Y-%m-%d %H:%M:%S'
    #
    # # Convert formatted timestamp string to datetime object
    # datetime_obj = datetime.strptime(timestamp_str, format_str)

    def get_trend(self, end_time):
        df = pd.read_excel("./infy_hour.xlsx", index_col=None)
        ltp = 0
        index = 0

        end_date_time = datetime.strptime(end_time.strftime(format_str), format_str)
        start_date_time = datetime.strptime(df.loc[0, 'Date'], format_str)
        subset_df = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'SMA', 'SIG'])
        while start_date_time <= end_date_time:
            subset_df = df.iloc[0:index].reset_index(drop=True)
            hourly_sma = subset_df.Close.rolling(21).mean()
            subset_df.loc[index, 'SMA'] = hourly_sma
            if hourly_sma != np.nan:
                if ltp > hourly_sma:
                    subset_df[index, 'SIG'] = 'BUY'
                else:
                    subset_df[index, 'SIG'] = 'SELL'
            index = index + 1
            ltp = subset_df.loc[-1:'Close']
            start_date_time = datetime.strptime(df.loc[index, 'Date'], format_str)
        trend = subset_df.iloc[:-3]
        print(trend)
