# investopedia-trading-api
An API, written in Python, for Investopedia's paper trading stock simulator.
Pull requests welcome!

## Dependencies

For this API to be useful you need an Investopedia trading account,
which you can make [here](http://www.investopedia.com/simulator/).

1. Python's mechanize library. See [here](http://wwwsearch.sourceforge.net/mechanize/).
2. Backported enum library for Python 2.7. See [here](https://pypi.python.org/pypi/enum34/).
3. Beautiful Soup. See [here](http://www.crummy.com/software/BeautifulSoup/bs4/doc/).


## Usage examples:

Import all the classes:
```python
from investopedia import *
```

Log into the simulator:
```python
client = Account("emailaddress","password")
```

Get account status (cash on hand, annual return, etc.):
```python
status = client.get_portfolio_status()
print status.account_val
print status.buying_power
print status.cash
print status.annual_return
```

Buying 10 shares of Google (GOOG) at market price:
```python
client.trade("GOOG", Action.buy, 10)
```

Selling 10 shares of Google at market price:
```python
client.trade("GOOG", Action.sell, 10)
```

Shorting 10 shares of Google:
```python
client.trade("GOOG", Action.short, 10)
```

Buying 10 shares of Google with a limit order at $500
```python
client.trade("GOOG", Action.buy, 10, "Limit", 500)
```
