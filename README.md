# investopedia-trading-api
An API, written in Python, for Investopedia's paper trading stock simulator.
Pull requests welcome.

For this API to be useful you need an Investopedia trading account,
and you can make one [here](http://www.investopedia.com/simulator/).

It also makes extensive use of Python's mechanize library, so you'll need
to install that as well. See [here](http://wwwsearch.sourceforge.net/mechanize/)

Some usage examples (assuming you've correctly imported the file and everything)

Logging into the simulator
```python
handle = investopedia.login("emailaddress","password")
```

Getting account status
```python
status = investopedia.getPortfolioStatus(handle)
print status
```

Buying 10 shares of Google (GOOG) at market price
```python
investopedia.trade(handle, "GOOG", 1, 10)
```

Selling 10 shares of Google at market price
```python
investopedia.trade(handle,"GOOG", 2, 10)
```

Buying 10 shares of Google with a limit order at $500
```python
investopedia.trade(handle,"GOOG", 1, 10, "Limit", 500)
```
