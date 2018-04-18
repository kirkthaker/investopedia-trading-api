# investopedia-trading-api
An API, written in Python, for Investopedia's paper trading stock simulator.
Pull requests welcome.

This library is now Python 3 compatible!

## Installation

For this API to be useful you need an Investopedia trading account,
which you can make [here](http://www.investopedia.com/simulator/).

You can install the library with pip:

`pip install InvestopediaApi`

## Documentation and examples:

Importing everything:
```python
from InvestopediaApi import ita
```

`ita` is the name of the file that contains everything of relevance for interacting with Investopedia.

The main class is `Account`, which logs you into the simulator upon instantiation.

Log into the simulator:
```python
from InvestopediaApi import ita
client = ita.Account("emailaddress", "password")
```

Currently, Investopedia Api has 4 "meta" functions:
1. `ita.Account.get_portfolio_status`
2. `ita.Account.get_current_securities`
3. `ita.Account.get_open_trades`
4. `ita.get_quote`

`get_portfolio_status` returns a named tuple with 4 elements: account_val, buying_power, cash, and annual_return.


```python
from InvestopediaApi import ita

client = ita.Account("email", "password")

status = client.get_portfolio_status()
print(status.account_val)
print(status.buying_power)
print(status.cash)
print(status.annual_return)
```


`get_current_securities` returns a Portfolio object with 3 attributes:
bought, shorted, and options. Each of those is a list of Security objects
with the following attributes:
symbol, description, quantity, purchase_price, current_price, current_value, and gain_loss


```python
from Investopedia import ita

client = ita.Account("email", "password")

portfolio = client.get_current_securities()

# Portfolio is not a list, it is a namedtuple object with 3 attributes: bought, shorted, options.
# Each of bought, shorted, and options is a list of Security objects, which have attributes
# symbol, description, quantity, purchase_price, current_price, current_value, and gain_loss

bought_securities = portfolio.bought
shorted_securities = portfolio.shorted
options = portfolio.options

for bought in bought_securities:
    print(bought.symbol)
    print(bought.description)
    print(bought.purchase_price)
    # etc.

# Repeat above loop for shorted securities and options
```

`get_open_trades` returns a list of "open" trades - that is, trades that have been made but not yet executed by the Investopedia platform. It returns a list of Trade namedtuple objects which have the following elements: date_time, description, symbol, and quantity.

```python
from InvestopediaApi import ita

client = ita.Account("email", "password")

open_trades = client.get_open_trades()

for open_trade in open_trades:
    print(open_trade.date_time)
    print(open_trade.description)
    print(open_trade.symbol)
    print(open_trade.quantity)
```

`get_quote` returns the price of a security given its symbol. Unlike the other 3 meta functions, this is not part of the Account class. Returns false if the security is not found or another error occurs.

```python
from InvestopediaApi import ita

client = ita.Account("email", "password")
print(ita.get_quote("GOOG"))
```

### Making trades

Of course, the most important function in this API is the `trade` function. This takes, at minimum, a security symbol (string), an orderType (Action class), and a quantity (integer).

The `trade` function is best illustrated with examples:

Buying 10 shares of Google (GOOG) at market price:
```python
client.trade("GOOG", ita.Action.buy, 10)
```

Selling 10 shares of Google at market price:
```python
client.trade("GOOG", ita.Action.sell, 10)
```

Shorting 10 shares of Google:
```python
client.trade("GOOG", ita.Action.short, 10)
```

Buying 10 shares of Google with a limit order at $500
```python
client.trade("GOOG", ita.Action.buy, 10, "Limit", 500)
```

You can browse through the code (it's only in one file) to get a more thorough understanding of the possibilities.

## Testing

All Tests: `python -m unittest discover`

### Feature Tests

Feature tests require a config file to be set up `InvestopediaApi/tests/config.py`. Instructions are in `InvestopediaApi/tests/config.example.py`.
