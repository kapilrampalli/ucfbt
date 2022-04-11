import pandas as pd
from ucfbt.results import standard_metrics
class Stock:
    def __init__(self, ticker, prices):
        self.ticker = ticker
        self.data = pd.read_csv(prices, parse_dates=True).sort_values("Date").reset_index(drop=True)
        self.index = 0
        self.signal_time = None
        self.position = 0
        self.limit_orders = set()

    def currData(self, colName):
        return self.data[colName][self.index]

    def market_buy(self, size, portfolio):
        if not self.tradeable():
            return
        if(self.ticker not in portfolio.keys()):
            portfolio[self.ticker] = 0
        portfolio[self.ticker] += size 
        portfolio["cash"] -= size * self.currData("Open")

    def market_sell(self, size, portfolio):
        if not self.tradeable():
            return
        if(self.ticker not in portfolio.keys()):
            portfolio[self.ticker] = 0
        portfolio[self.ticker] -= size
        portfolio["cash"] += size * self.currData("Open")

    def limit_buy(self, price, size):
        if not self.tradeable():
            return
        self.limit_orders.add(("b", price, size))

    def limit_sell(self, price, size):
        if not self.tradeable():
            return
        self.limit_orders.add(("s", price, size))
        
    def tradeable(self):
        if self.data["Date"][0] < self.signal_time < self.data["Date"][len(self.data) - 1]:
            return True
        return False

    def update(self, newTime, portfolio):
        fills = []
        while(self.currData("Date") < newTime):
            cur_index = len(fills)
            for bs, price, size in self.limit_orders:
                if(self.currData("Low") <= price <= self.currData("High")):
                    if self.ticker not in portfolio:
                        portfolio[self.ticker] = 0
                    portfolio[self.ticker] += size if bs == "b" else -size
                    fills.append((bs, price, size))
            for i in range(cur_index, len(fills)):
                self.limit_orders.remove(fills[i])
            self.index += 1
        self.signal_time = newTime
        return fills        

    def get_value(self, portfolio):
        try:
            return portfolio[self.ticker] * self.currData("Close")
        except:
            print("{} stock not in portfolio".format(self.ticker))
            return 0

def backtest(init, update, assets, signal):
    ctx = {}
    init(ctx)
    portfolio = {"cash": 100000}
    portfolio_history = pd.DataFrame(index = signal.index, columns = ["time"] + [asset.ticker for asset in assets])
    value_history = pd.DataFrame(index = signal.index, columns = ["time", "value"])
    portfolio_history["time"] = signal["time"]
    value_history["time"] = signal["time"]
    for index, row in signal.iterrows(): 
        for asset in assets:
            print(signal.loc[index])
            asset.update(signal.loc[index]["time"], portfolio)
        update(ctx, portfolio, assets, row) 
        for asset in assets:
            if asset.ticker in portfolio:
                portfolio_history.loc[index][asset.ticker] = portfolio[asset.ticker]
        value = portfolio["cash"]
        for asset in assets:
            value += asset.get_value(portfolio)
        value_history.loc[index]["value"] = value
    return portfolio_history, value_history   




def init(ctx):
    pass
def update(ctx, portfolio, assets, signal):
    if "AAPL" not in portfolio:
        assets[0].limit_buy(170, 1)

    
portfolio_history, value_history = backtest(init, update, [Stock("AAPL", "dummy.csv") ], pd.read_csv("signal.csv", parse_dates=True).sort_values("time").reset_index(drop=True))
standard_metrics(portfolio_history, value_history)


"""
- fees
- options
- slippage
- 
"""