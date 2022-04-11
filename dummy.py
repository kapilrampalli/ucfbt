import pandas as pd
from ucfbt.backtest import backtest, create_portfolio
from ucfbt.assets.stock import Stock
from ucfbt.results import standard_metrics

def init(ctx):
    pass
def update(ctx, portfolio, assets, signal):
    if "AAPL" not in portfolio:
        assets[0].market_order(1)

portfolio = create_portfolio()
aapl = Stock("AAPL", pd.read_csv("dummy.csv", parse_dates=True).sort_values("Date").reset_index(drop=True), portfolio)
signal = pd.read_csv("signal.csv", parse_dates=True).sort_values("time").reset_index(drop=True)
portfolio_history, value_history = backtest(init, update, [aapl], signal, portfolio)
print(value_history)
standard_metrics(portfolio_history, value_history)


"""
- options
- slippage
"""