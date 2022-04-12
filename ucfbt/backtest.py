import pandas as pd

def create_portfolio(cash=100000, margin=100000):
    return {"cash": cash, "margin": margin}

def backtest(init, update, assets, signal, portfolio):
    ctx = {}
    init(ctx)

    portfolio_history = pd.DataFrame(index = signal.index, columns = ["time"] + [asset.ticker for asset in assets])
    value_history = pd.DataFrame(index = signal.index, columns = ["time", "value"])
    portfolio_history["time"] = signal["time"]
    value_history["time"] = signal["time"]
    for index, row in signal.iterrows(): 
        for asset in assets:
            asset.time_update(signal.loc[index]["time"])
        update(ctx, portfolio, assets, row) 
        for asset in assets:
            if asset.ticker in portfolio:
                portfolio_history.loc[index, asset.ticker, ] = portfolio[asset.ticker]
        value = portfolio["cash"]
        for asset in assets:
            value += asset.get_value(portfolio)
        value_history.loc[index, "value"] = value
    return portfolio_history, value_history       
