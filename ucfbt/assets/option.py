from tokenize import Double
import pandas as pd
from ucfbt.assets.asset  import Asset

class Option(Asset):
    def __init__(self, ticker, prices_df, portfolio, underlying):
        super().__init__(ticker, prices_df, portfolio)
        self.limit_orders = set()
        self.underlying = underlying
        self.strike = int(self.ticker[-8:])/1000.0
        self.type = "Call" if self.ticker[-9] == 'C' else "Put"
    
    def market_buy(self, size):
        self.market_order(size)
    def market_sell(self, size):
        self.market_order(-size)
    def limit_buy(self, price, size):
        self.limit_order(price, size)
    def limit_sell(self, price, size):
        self.limit_order(price, -size)

    def market_order(self, size):
        if not self.tradeable():
            return
        self.change_position( self.currData("Open"), size)

    def limit_order(self, price, size):
        if not self.tradeable():
            return
        self.limit_orders.add((price, size))

    def get_limit_orders(self):
        return self.limit_orders
         
    def tradeable(self):
        if self.data["Date"][0] < self.signal_time < self.data["Date"][len(self.data) - 1]:
            return True
        return False

    def time_update(self, newTime):
        fills = []
        if not self.tradeable() and self.ticker in self.portfolio:
            del self.portfolio[self.ticker]
        while(self.currData("Date") < newTime):
            cur_index = len(fills)
            if(self.ticker in self.portfolio):
                if(self.type == "Call" and self.strike <= self.underlying.currData("High")):
                    self.portfolio["cash"] -= self.portfolio[self.ticker] * 100 * (self.underlying.currData("High") - self.strike)
                    del self.portfolio[self.ticker]
                if(self.type == "Put" and self.strike >= self.underlying.currData("Low")):
                    if self.underlying.ticker not in self.portfolio:
                        self.portfolio[self.underlying.ticker] = 0
                    self.portfolio[self.underlying.ticker] += self.portfolio[self.ticker] * 100
                    self.portfolio["cash"] -= self.portfolio[self.ticker] * 100 * (self.strike)
                    del self.portfolio[self.ticker]
            for price, size in self.limit_orders:
                if(self.currData("Low") <= price <= self.currData("High")):
                    self.change_position(price, size)
                    fills.append((price, size))
            for i in range(cur_index, len(fills)):
                self.limit_orders.remove(fills[i])
            self.index += 1
        self.signal_time = newTime       
    
    def change_position(self, price, size):
        self.portfolio["cash"] -= size * price
        self.portfolio["cash"] -= self.feeModel(size)
        if self.ticker not in self.portfolio:
            self.portfolio[self.ticker] = 0
        self.portfolio[self.ticker] += size 

    def get_value(self, portfolio):
        try:
            return portfolio[self.ticker] * self.currData("Close")
        except:
            print("{} option not in portfolio".format(self.ticker))
            return 0
    
    def feeModel(self, size):
        return 0.65 * size
    
        