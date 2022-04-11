import pandas as pd
import numpy as np

# Be able to read OHLC data from CSV into a pandas dataframe
def read_candlestick_data(file):
    dframe = pd.read_csv(file)

    # replace with corresponding column names from csv
    date_col = 'Date'
    open_col = 'Open'
    high_col = 'High'
    low_col = 'Low'
    close_col = 'Close'

    column_dict = {'Date': date_col, 'Open' : open_col, 'High' : high_col, 'Low' : low_col, 'Close' : close_col}
    dframe = dframe.sort_values(column_dict['Date'])
    dframe = dframe.reset_index(drop=True)
    if not ":" in dframe[column_dict['Date']][0]:
        #if dealing with non-timestamp data, fill in hours and minutes column
        #with market close for your time zone, default CST
        dframe[column_dict['Date']] = pd.to_datetime(dframe[column_dict['Date']]) + pd.DateOffset(hours=15,minutes=0)
    else:
        dframe[column_dict['Date']] = pd.to_datetime(dframe[column_dict['Date']])
    dframe = dframe[[column_dict['Date'], column_dict['Open'], column_dict['High'], column_dict['Low'], column_dict['Close']]]
    return dframe