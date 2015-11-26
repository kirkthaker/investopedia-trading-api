# investopedia-trading-api
An API, written in Python, for Investopedia's paper trading stock simulator.
Pull requests welcome!

For this API to be useful you need an Investopedia trading account,
and you can make one [here](http://www.investopedia.com/simulator/).

It also makes extensive use of Python's mechanize library, so you'll need
to install that as well. See [here](http://wwwsearch.sourceforge.net/mechanize/).

You'll also need to backported enum library for Python 2.7. See [here](https://pypi.python.org/pypi/enum34/).

Some usage examples:

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
status = client.getPortfolioStatus()
print status
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
