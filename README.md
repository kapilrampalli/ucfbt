# Basic Strategy
```python
def init(ctx):
    # Should initialize all of the book-keeping structures that it needs

def update(ctx, signal_name, signal_data):
    # Should handle updates

results = backtest(init, update, prices={"ticker": ticker_dataframe_ohlc}, signals={"signal": signal_dataframe})
```