import pandas as pd
from ucfbt.backtest import backtest, create_portfolio
from ucfbt.assets.stock import Stock
from ucfbt.results import standard_metrics
from ucfbt.data import read_candlestick_data
def init(ctx):
    pass
def update(ctx, portfolio, assets, signal):
    if "AAPL" not in portfolio:
        assets[0].market_order(1)

portfolio = create_portfolio()
aapl = Stock("AAPL", read_candlestick_data("dummy.csv"), portfolio)
signal =  read_candlestick_data("dummy.csv")
signal["time"] = signal["Date"]
portfolio_history, value_history = backtest(init, update, [aapl], signal, portfolio)
portfolio_history = portfolio_history.fillna(0)
print(value_history)
standard_metrics(portfolio_history, value_history)


"""
- options
- slippage
"""