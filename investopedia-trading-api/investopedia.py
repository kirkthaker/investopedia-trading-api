import mechanicalsoup
from enum import Enum
from collections import namedtuple
from bs4 import BeautifulSoup
import re


Status = namedtuple("Status", "account_val buying_power cash annual_return")
Portfolio = namedtuple("Portfolio", "bought options shorted")
Security = namedtuple("Security", "symbol description quantity purchase_price current_price current_value")
Trade = namedtuple("Trade", "date_time description symbol quantity")


class Action(Enum):
    buy = 1
    sell = 2
    short = 3
    cover = 4


class Duration(Enum):
    day_order = 1
    good_cancel = 2


class Account:
    BASE_URL = 'http://www.investopedia.com'

    def __init__(self, email, password):
        """
        Logs a user into Investopedia's trading simulator,
        given a *username* and *password*.
        """

        self.br = br = mechanicalsoup.Browser()
        login_page = self.fetch("/accounts/login.aspx?returnurl=http://www.investopedia.com/simulator/")

        # you have to select the form before you can input information to it
        # the login form used to be at nr=2, now it's at nr=0
        login_form = login_page.soup.select("form#account-api-form")[0]
        login_form.select("#edit-email")[0]["value"] = email
        login_form.select("#edit-password")[0]["value"] = password
        br.submit(login_form, login_page.url)

    def fetch(self, url):
        url = '%s%s' % (self.BASE_URL, url)
        return self.br.get(url)

    def get_portfolio_status(self):
        """
        Returns a Status object containing account value,
        buying power, cash on hand, and annual return.
        Annual return is a percentage.
        """

        response = self.fetch('/simulator/portfolio/')

        parsed_html = response.soup

        # The ids of all the account information values
        acct_val_id = "ctl00_MainPlaceHolder_currencyFilter_ctrlPortfolioDetails_PortfolioSummary_lblAccountValue"
        buying_power_id = "ctl00_MainPlaceHolder_currencyFilter_ctrlPortfolioDetails_PortfolioSummary_lblBuyingPower"
        cash_id = "ctl00_MainPlaceHolder_currencyFilter_ctrlPortfolioDetails_PortfolioSummary_lblCash"
        return_id = "ctl00_MainPlaceHolder_currencyFilter_ctrlPortfolioDetails_PortfolioSummary_lblAnnualReturn"

        # Use BeautifulSoup to extract the relevant values based on html ID tags
        account_value = parsed_html.find('span', attrs={'id': acct_val_id}).text
        buying_power = parsed_html.find('span', attrs={'id': buying_power_id}).text
        cash = parsed_html.find('span', attrs={'id': cash_id}).text
        annual_return = parsed_html.find('span', attrs={'id': return_id}).text

        # We want our returned values to be floats
        # Use regex to remove non-numerical or decimal characters
        # But keep - (negative sign)
        regexp = "[^0-9.-]"
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

    def get_current_securities(self):
        """
        Returns a Portfolio object containing:
        bought securities, options, and shorted securities
        Each of theses are lists of Securities objects containing:
        symbol description quantity purchase_price current_price current_value gain_loss
        """
        response = self.fetch('/simulator/portfolio/')
        soup = BeautifulSoup(response.content, "html.parser")

        stock_table = soup.find("table", id="stock-portfolio-table").find("tbody")
        option_table = soup.find("table", id="option-portfolio-table").find("tbody")
        short_table = soup.find("table", id="short-portfolio-table").find("tbody")

        if stock_table is not None:
            stock_list = stock_table.find_all("tr")[:-1]
            stock_list = [s.find_all("td")[-8:-2] for s in stock_list]
        else:
            stock_list = []

        if option_table is not None:
            option_list = option_table.find_all("tr")[:-1]
            option_list = [o.find_all("td")[-8:-2] for o in option_list]
        else:
            option_list = []

        if short_table is not None:
            short_list = short_table.find_all("tr")[:-1]
            short_list = [s.find_all("td")[-8:-2] for s in short_list]
        else:
            short_list = []

        bought = []
        options = []
        shorted = []

        for stock_data in stock_list:
            stock_data_text = [s.getText() for s in stock_data]
            if len(stock_data_text) == 6:
                sec = Security(
                    symbol=stock_data_text[0],
                    description=stock_data_text[1],
                    quantity=int(stock_data_text[2]),
                    purchase_price=float(stock_data_text[3][1:].replace(",", "")),
                    current_price=float(stock_data_text[4][1:].replace(",", "")),
                    current_value=float(stock_data_text[5][1:].replace(",", ""))
                )
                bought.append(sec)

        for option_data in option_list:
            option_data_text = [o.getText() for o in option_data]
            if len(option_data_text) == 6:
                sec = Security(
                    symbol=option_data_text[0],
                    description=option_data_text[1],
                    quantity=int(option_data_text[2]),
                    purchase_price=float(option_data_text[3][1:].replace(",", "")),
                    current_price=float(option_data_text[4][1:].replace(",", "")),
                    current_value=float(option_data_text[5][1:].replace(",", ""))
                )
                options.append(sec)

        for short_data in short_list:
            short_data_text = [s.getText() for s in short_data]
            if len(short_data_text) == 6:
                sec = Security(
                    symbol=short_data_text[0],
                    description=short_data_text[1],
                    quantity=int(short_data_text[2]),
                    purchase_price=float(short_data_text[3][1:].replace(",", "")),
                    current_price=float(short_data_text[4][1:].replace(",", "")),
                    current_value=float(short_data_text[5][1:].replace(",", ""))
                )
                shorted.append(sec)

        return Portfolio(
            bought=bought,
            options=options,
            shorted=shorted
        )

    def get_open_trades(self):
        """
        Return a list of Trade objects that represent open trades (orders
        that have been made but not yet fulfilled).
        """
        response = self.fetch('/simulator/trade/showopentrades.aspx')
        soup = BeautifulSoup(response.content, "html.parser")

        # Case: No pending trades
        if soup.find("table", class_="table1") is None:
            return []

        open_trades_table = soup.find("table", class_="table1").find("tbody")
        open_trades_list = open_trades_table.find_all("tr", class_="table_data")

        open_trades_raw = []
        for open_trade in open_trades_list:
            trade_info_list = open_trade.find_all("td")
            open_trades_raw.append([i.getText() for i in trade_info_list][2:6])

        open_trades = []
        for raw_data in open_trades_raw:
            trade_obj = Trade(
                date_time=raw_data[0],
                description=raw_data[1],
                symbol=raw_data[2],
                quantity=int(raw_data[3])
            )
            open_trades.append(trade_obj)

        return open_trades

    def trade(self, symbol, orderType, quantity, priceType="Market", price=False, duration=Duration.good_cancel):
        """
        Executes trades on the platform. See the readme.md file
        for examples on use and inputs. Returns True if the
        trade was successful. Else an exception will be
        raised.

        client.trade("GOOG", Action.buy, 10)
        client.trade("GOOG", Action.buy, 10, "Limit", 500)
        """

        br = self.br
        trade_page = self.fetch('/simulator/trade/tradestock.aspx')
        trade_form = trade_page.soup.select("form#orderForm")[0]

        # input symbol, quantity, etc.
        trade_form.select("input#symbolTextbox")[0]["value"] = symbol
        trade_form.select("input#quantityTextbox")[0]["value"] = str(quantity)

        # input transaction type
        [option.attrs.pop("selected", "") for option in trade_form.select("select#transactionTypeDropDown")[0]("option")]
        trade_form.select("select#transactionTypeDropDown")[0].find("option", {"value": str(orderType.value)})["selected"] = True

        # input price type
        [radio.attrs.pop("checked", "") for radio in trade_form("input", {"name": "Price"})]
        trade_form.find("input", {"name": "Price", "value": priceType})["checked"] = True

        # input duration type
        [option.attrs.pop("selected", "") for option in trade_form.select("select#durationTypeDropDown")[0]("option")]
        trade_form.select("select#durationTypeDropDown")[0].find("option", {"value": str(duration.value)})["selected"] = True

        # if a limit or stop order is made, we have to specify the price
        if price and priceType == "Limit":
            trade_form.select("input#limitPriceTextBox")[0]["value"] = str(price)

        elif price and priceType == "Stop":
            trade_form.select("input#stopPriceTextBox")[0]["value"] = str(price)

        prev_page = br.submit(trade_form, trade_page.url)
        prev_form = prev_page.soup.find("form", {"name": "simTradePreview"})
        br.submit(prev_form, prev_page.url)

        return True


def get_quote(symbol):
    BASE_URL = 'http://www.investopedia.com'
    """
    Returns the Investopedia-delayed price of a given security,
    represented by its stock symbol, a string. Returns false if
    security not found or if another error occurs.
    """
    br = mechanicalsoup.Browser()
    response = br.get(BASE_URL + '/markets/stocks/' + symbol.lower())
    quote_id = "quotePrice"
    parsed_html = response.soup
    try:
        quote = parsed_html.find('td', attrs={'id': quote_id}).text
    except:
        return False
    return float(quote)
