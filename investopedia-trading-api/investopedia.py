import mechanize
from enum import Enum
from collections import namedtuple
from bs4 import BeautifulSoup
import re


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
        """
        Logs a user into Investopedia's trading simulator,
        given a *username* and *password*.
        """

        self.br = br = mechanize.Browser()
        self.fetch("/accounts/login.aspx?returnurl=http://www.investopedia.com/simulator/")

        # you have to select the form before you can input information to it
        # the login form used to be at nr=2, now it's at nr=0
        br.select_form(nr=0)
        br.form["email"] = email
        br.form["password"] = password
        br.submit()

    def fetch(self, url):
        url = '%s%s' % (self.BASE_URL, url)
        return self.br.open(url)

    def get_portfolio_status(self):
        """
        Returns a Status object containing account value,
        buying power, cash on hand, and annual return.
        Annual return is a percentage.
        """

        response = self.fetch('/simulator/portfolio/')
        html = response.read()
        parsed_html = BeautifulSoup(html, "html.parser")

        # The ids of all the account information values
        acct_val_id = "ctl00_MainPlaceHolder_currencyFilter_ctrlPortfolioDetails_PortfolioSummary_lblAccountValue"
        buying_power_id= "ctl00_MainPlaceHolder_currencyFilter_ctrlPortfolioDetails_PortfolioSummary_lblBuyingPower"
        cash_id = "ctl00_MainPlaceHolder_currencyFilter_ctrlPortfolioDetails_PortfolioSummary_lblCash"
        return_id = "ctl00_MainPlaceHolder_currencyFilter_ctrlPortfolioDetails_PortfolioSummary_lblAnnualReturn"

        # Use BeautifulSoup to extract the relevant values based on html ID tags
        account_value = parsed_html.find('span', attrs={'id':acct_val_id}).text
        buying_power = parsed_html.find('span', attrs={'id':buying_power_id}).text
        cash = parsed_html.find('span', attrs={'id':cash_id}).text
        annual_return = parsed_html.find('span', attrs={'id':return_id}).text

        # We want our returned values to be floats
        # Use regex to remove non-numerical or decimal characters
        regexp = "[^0-9.]"
        account_value = float(re.sub(regexp, '', account_value))
        buying_power = float(re.sub(regexp, '', buying_power))
        cash = float(re.sub(regexp, '', cash))
        annual_return = float(re.sub(regexp, '', annual_return))

        return Status(
            account_val=account_value,
            buying_power=buying_power,
            cash=cash,
            annual_return=annual_return,
        )

    def trade(self, symbol, orderType, quantity, priceType="Market", price=False, duration=Duration.good_cancel):
        """
        Executes trades on the platform. See the readme.md file
        for examples on use and inputs. Returns True if the
        trade was successful. Else an exception will be
        raised.
        """

        self.fetch('/simulator/trade/tradestock.aspx')
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
        elif price is not False:
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
