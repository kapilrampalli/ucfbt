# Add any other metrics that seem important
# For each metric:
#   - Make a function that takes in results and prints/plots stuff
# Stuff to include:
# - Sharpe/Sartino Ratio
# - Max Drawdown
# - Plotting candlestick data with matplotlib
# - Plot portfolio value

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.pyplot import figure
import datetime as dt


def standard_metrics(portfolio_history, value_history):
    # print("RETURNS:")
    # print(value_history)
    returns_hold = pd.Series(value_history['value']).pct_change()
    # print("PCT CHANGE:")
    # print(returns_hold)
    sharpe = returns_hold.aggregate(sharpe_ratio)
    sort = returns_hold.aggregate(sortino)
    # print("Sharpe: ", sharpe)
    # print("Sortino: ", sort)

    figure(figsize=(15, 6))
    x = value_history['time']
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=int(len(x) / 10)))
    plt.plot(x,value_history['value'])
    plt.gcf().autofmt_xdate()
    plt.xlabel("Date")
    plt.ylabel("Value")
    
    plt.show()

def annualize_rets(r, periods_per_year):
    """
    Annualizes a set of returns
    We should infer the periods per year
    but that is currently left as an exercise
    to the reader :-)
    """
    compounded_growth = (1+r).prod()
    n_periods = r.shape[0]
    return compounded_growth**(periods_per_year/n_periods)-1

def annualize_vol(r, periods_per_year):
    """
    Annualizes the vol of a set of returns
    We should infer the periods per year
    but that is currently left as an exercise
    to the reader :-)
    """
    return r.std()*(periods_per_year**0.5)

def sharpe_ratio(r, riskfree_rate=0.03, periods_per_year=252):  
    """
    Computes the annualized sharpe ratio of a set of returns
    """
    # convert the annual riskfree rate to per period
    rf_per_period = (1+riskfree_rate)**(1/periods_per_year)-1
    excess_ret = r - rf_per_period
    ann_ex_ret = annualize_rets(excess_ret, periods_per_year)
    ann_vol = annualize_vol(r, periods_per_year)
    return ann_ex_ret/ann_vol

def sortino(r, riskfree_rate=0.03, periods_per_year=252):
    rf_per_period = (1+riskfree_rate)**(1/periods_per_year)-1
    excess_ret = r - rf_per_period
    ann_ex_ret = annualize_rets(excess_ret, periods_per_year)
    neg_ann_vol = annualize_vol(r[r<0], periods_per_year)

    return ann_ex_ret/neg_ann_vol

