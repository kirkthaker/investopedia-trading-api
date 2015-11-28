# A class for executing trades on Investopedia's Stock simulator
# Makes use of Python's mechanize library
import mechanize
from enum import Enum
from collections import namedtuple


class Action(Enum):
    buy = 1
    sell = 2
    short = 3
    cover = 4


class Duration(Enum):
    day_order = 1
    good_cancel = 2


Status = namedtuple("Status", "account_val buying_power cash annual_return")


class Account:
    BASE_URL = 'http://www.investopedia.com'

    def __init__(self, email, password):
        # Logs a user into Investopedia's trading simulator
        # It takes their username & password and returns a handler called br
        # br can then be used to execute trades.

        self.br = br = mechanize.Browser()
        self.go("/accounts/login.aspx?returnurl=http://www.investopedia.com/simulator/")

        # you have to select the form before you can input information to it
        # the login form happens to be at nr=2
        br.select_form(nr=2)
        br.form["email"] = email
        br.form["password"] = password
        br.submit()

    def go(self, url):
        url = '%s%s' % (self.BASE_URL, url)
        return self.br.open(url)

    def get_portfolio_status(self):
        # This function takes our mechanize handle and returns:
        # account value, buying power, cash on hand, and annual return
        # Annual return is a percentage, not a decimal

        response = self.go('/simulator/portfolio/')
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

        return Status(
            account_val=account_value,
            buying_power=buying_power_value,
            cash=cash_value,
            annual_return=return_value,
        )

    def trade(self, symbol, orderType, quantity, priceType="Market", price=False, duration=Duration.good_cancel):
        # This function executes trades on the platform
        # See the readme.md file for examples on use and inputs
        # It outputs True if the trade was successful and False if it was not.

        self.go(self.url('/simulator/trade/tradestock.aspx'))
        handle = self.br
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

        return True
