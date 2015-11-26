# A class for executing trades on Investopedia's Stock simulator
# Makes use of Python's mechanize library
import mechanize
from enum import Enum

class Action(Enum):
    buy = 1
    sell = 2
    short = 3
    cover = 4

class Duration(Enum):
    day_order = 1
    good_cancel = 2

class Account:
    def __init__(self, email, password):
        # Logs a user into Investopedia's trading simulator
        # It takes their username & password and returns a handler called br
        # br can then be used to execute trades.

        br = mechanize.Browser()
        url = "http://www.investopedia.com/accounts/login.aspx?returnurl=http://www.investopedia.com/simulator/"
        br.open(url)

        # you have to select the form before you can input information to it
        # the login form happens to be at nr=2
        br.select_form(nr=2)

        br.form["email"] = email
        br.form["password"] = password

        br.submit()

        # return the handle, br, so that we can use it later on for trading, etc.
        self.br = br

    def getPortfolioStatus(self):
        handle = self.br
        # This function takes our mechanize handle and returns:
        # account value, buying power, cash on hand, and annual return
        # Annual return is a percentage, not a decimal

        account_url = "http://www.investopedia.com/simulator/portfolio/"
        response = handle.open(account_url)

        html = response.read()

        # The ids of all the account information values
        acct_val_str = "ctl00_MainPlaceHolder_currencyFilter_ctrlPortfolioDetails_PortfolioSummary_lblAccountValue"
        buying_power_str = "ctl00_MainPlaceHolder_currencyFilter_ctrlPortfolioDetails_PortfolioSummary_lblBuyingPower"
        cash_str = "ctl00_MainPlaceHolder_currencyFilter_ctrlPortfolioDetails_PortfolioSummary_lblCash"
        return_str = "ctl00_MainPlaceHolder_currencyFilter_ctrlPortfolioDetails_PortfolioSummary_lblAnnualReturn"
        # The values all end with the HTML tag "span"
        end_str = "</span>"

        # Get the beginning and ending points, then simply slice out the string.
        # Simply use the find function to get the required values
        # This could probably be more elegant...
        acct_begin = html.find(acct_val_str)
        acct_end = html.find(end_str, acct_begin)
        account_value = html[acct_begin + len(acct_val_str) + 3:acct_end]
        account_value = float(account_value.replace(',', ''))

        buying_power_begin = html.find(buying_power_str)
        buying_power_end = html.find(end_str, buying_power_begin)
        buying_power_value = html[buying_power_begin + len(buying_power_str) + 3:buying_power_end]
        buying_power_value = float(buying_power_value.replace(',', ''))

        cash_begin = html.find(cash_str)
        cash_end = html.find(end_str, cash_begin)
        cash_value = html[cash_begin + len(cash_str) + 3:cash_end]
        cash_value = float(cash_value.replace(',', ''))

        return_begin = html.find(return_str)
        return_end = html.find(end_str, return_begin)
        return_value = html[return_begin + len(return_str) + 4:return_end-1]
        return_value = float(return_value.replace('%', ''))

        return account_value, buying_power_value, cash_value, return_value


    def trade(self, symbol, orderType, quantity, priceType="Market", price=False, duration=Duration.good_cancel):
        # This function executes trades on the platform
        # It takes the following inputs:

        # 1. handle - this is what the function login(username, password) returns.
        # You need it because it contains the logged in session information

        # 2. symbol - symbol of the security ("GOOG", "AAPL", etc.).
        # Type is string.

        # 3. orderType - 1 is buy, 2 is sell, 3 is sell short, 4 is buy to cover
        # Type is int.

        # 4. quantity - number of shares to buy.
        # Type is int.

        # 5. priceType - Type of pricing: Market, Limit, or Stop. Case sensitive.
        # Type is string.

        # 6. price - If you're executing a Limit/Stop order - the price wanted.
        # Type is float.

        # duration - How long it's valid (good until cancelled is 2, day order is 1)
        # Type is int.

        # It returns a boolean called result that is true if trading was successful
        # and false if it was not.

        #open the trading page and select the trading form
        handle = self.br
        result = True

        try:
            trading_url = "http://www.investopedia.com/simulator/trade/tradestock.aspx"
            handle.open(trading_url)
            handle.select_form(name="simTrade")

            # input order type, quantity, etc.
            handle.form["symbolTextbox"] = symbol
            handle.form["quantityTextbox"] = str(quantity)
            handle.form["transactionTypeDropDown"] = [str(orderType.value)]
            handle.form["Price"] = [priceType]
            handle.form["durationTypeDropDown"] = [str(duration.value)]

            # no price to specify - we'll take the market price.
            if priceType == "Market":
                handle.submit()
                handle.select_form(name="simTradePreview")
                handle.submit()

            # if a limit or stop order is made, we have to specify the price
            elif price != False:
                if priceType == "Limit":
                    handle.form["limitPriceTextBox"] = str(price)
                elif priceType == "Stop":
                    handle.form["stopPriceTextBox"] = str(price)
                # submit the form and then submit the "preview order" page that follows
                # (that's why we have two "submits")
                handle.submit()
                handle.select_form(name="simTradePreview")
                handle.submit()
        except:
            result = False

        return result
