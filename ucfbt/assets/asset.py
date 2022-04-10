class Asset:
    def __init__(self, ticker, prices_df, portfolio, transformFunc = lambda x : x):
        self.ticker = ticker
        self.data = prices_df
        self.index = 0
        self.signal_time = None
        self.position = 0
        self.portfolio = portfolio
        self.priceTransform = transformFunc
    
    def currData(self, colName):
        return self.data[colName][self.index]
    
    def tradeable(self):
        pass

    def time_update(self, newTime):
        pass
    
    def feeModel(self, size):
        pass
    
    def slippage(self, price):
        return self.priceTransform(price)


# Assets can be "complete"