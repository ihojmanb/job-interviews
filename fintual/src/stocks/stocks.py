import json
from functools import reduce
from datetime import datetime
import math

# Setup
stocks_database = open("fake_data.json")
stocks_database = json.load(stocks_database)
available_tickers = [stock["ticker"] for stock in stocks_database]


class Stock:
    def __init__(self, symbol, amount) -> None:
        self._symbol = symbol
        self._amount = amount

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        self._symbol = symbol

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = amount

    def price(self, date: str):
        stock_price = self.get_stock_price_from_database(date)
        return stock_price

    def get_stock_price_from_database(self, date):
        if self.symbol in available_tickers:
            stock_data = self.get_stock_from_database()
            stock_price = stock_data[0]["prices"][date]
            return stock_price
        else:
            raise KeyError("ticker is not in our database.")

    def get_stock_from_database(self):
        stock_data = [
            stock for stock in stocks_database
            if stock["ticker"] == self.symbol
        ]
        return stock_data


class Portfolio:
    def __init__(self, stock_collection: dict) -> None:
        self._stocks = self.set_stock_collection(stock_collection)
        self.utils = PortfolioUtils()

    @property
    def stocks(self):
        return self._stocks

    def set_stock_collection(self, stock_dict):
        stock_collection = []
        for symbol, amount in stock_dict.items():
            stock_collection.append(Stock(symbol, amount))
        return stock_collection

    def profit(self, init_date, end_date):

        list_of_total_stocks_buy_prices = self.get_total_stocks_prices(
            init_date)
        list_of_total_stocks_sell_prices = self.get_total_stocks_prices(
            end_date)

        profit = self._calculate_profit(
            list_of_total_stocks_buy_prices, list_of_total_stocks_sell_prices)
        return profit

    def get_total_stocks_prices(self, date):
        list_of_stocks_amount = self.get_stocks_amount()
        list_of_stocks_prices = self.get_stocks_prices(date)
        list_of_total_stocks_prices = self.multiply_stock_prices_by_amounts(
            list_of_stocks_prices, list_of_stocks_amount)
        return list_of_total_stocks_prices

    def _calculate_profit(self, stocks_buy_prices, stocks_sell_prices):
        list_of_profit_by_stock = self.substract_buy_to_sell_prices(
            stocks_buy_prices, stocks_sell_prices)
        profit = self.sum_stock_profits(list_of_profit_by_stock)
        return profit

    def get_stocks_amount(self):
        return list(map(lambda stock: stock.amount, self.stocks))

    def get_stocks_prices(self, date):
        stocks_prices = list(map(lambda stock: stock.price(date), self.stocks))
        return stocks_prices

    def multiply_stock_prices_by_amounts(self, stocks_buy_prices,
                                         stocks_amount):
        return [a*b for a, b in zip(stocks_buy_prices, stocks_amount)]

    def substract_buy_to_sell_prices(self,
                                     list_of_total_stocks_buy_prices,
                                     list_of_total_stocks_sell_prices):

        return [a-b for a, b in zip(list_of_total_stocks_sell_prices,
                                    list_of_total_stocks_buy_prices)]

    def sum_stock_profits(self, list_of_profit_by_stock):
        profit = reduce(lambda x, y: x + y, list_of_profit_by_stock)
        return profit

    def annualized_return(self, initial_date, ending_date, measure="year"):

        initial_investment = self.sum_stock_profits(
            self.get_total_stocks_prices(initial_date))

        profit = self.profit(initial_date, ending_date)
        # R
        investment_return = profit/initial_investment
        # t
        time_between_dates = self.utils.get_time_between(
            initial_date, ending_date, measure=measure, format="%Y-%m-%d")
        # r
        annualized_return = math.pow(
            (1 + investment_return), 1/time_between_dates) - 1
        return annualized_return


# Utility class for helper method that are out of the business logic of
# Portfolio Class
# TODO refactor this class, altough not a core component.
class PortfolioUtils:
    def __init__(self):
        pass

    def get_time_between(self, initial_date, ending_date, measure: str, format: str):
        days_between_dates = self.get_days_between(
            initial_date, ending_date, format)

        if measure == "day":
            return days_between_dates

        elif measure == "month":
            months_between_dates = round((days_between_dates / 365) * 12, 3)
            # months_between_dates = self.get_rounded("month", days_between_dates)
            return months_between_dates

        elif measure == "year":
            years_between_dates = round((days_between_dates / 365), 3)
            # years_between_dates = self.get_rounded("year", days_between_dates)
            return years_between_dates

    def get_rounded(self, measure, time):
        if measure == "month":
            return self.get_rounded_month(time)
        elif measure == "year":
            return self.get_rounded_year(time)
  
    def get_rounded_month(self, days_between_dates):
        amount= (days_between_dates / 365) * 12
        return self.non_zero_round_calculator(amount)

    def get_rounded_year(self, days_between_dates):
        amount= days_between_dates / 365
        return self.non_zero_round_calculator(amount)

    def non_zero_round_calculator(self, amount):
        total_digits = 2
        rounded_days_between_dates = round(amount, total_digits)
        while rounded_days_between_dates == 0:
            total_digits += 1
            rounded_days_between_dates = round(amount, total_digits)
        return rounded_days_between_dates  



    def get_days_between(self, initial_date, ending_date, format: str):
        initial_datetime_object = self.transform_string_date_to_datetime(
            initial_date, format)
        ending_datetime_object = self.transform_string_date_to_datetime(
            ending_date, format)

        delta_time_object = abs(
            ending_datetime_object - initial_datetime_object)

        days_between_dates = delta_time_object.days

        return days_between_dates

    def transform_string_date_to_datetime(self, date, format):
        return datetime.strptime(date, format)

    def report_annualized_return(self, initial_date, ending_date, annualized_return):
        format = "%Y-%m-%d"
        days_between_dates = self.get_days_between(
            initial_date, ending_date, format)
        if days_between_dates <= 31:
            return self.report(annualized_return, measure="day")

        elif days_between_dates > 31 and days_between_dates < 365:
            return self.report(annualized_return, measure="month")

        elif days_between_dates >= 365:
            return self.report(annualized_return, measure="year")

    def report(self, annualized_return, measure: str):
        report = f"""annualized return is {round(annualized_return*100, 2)}% per {measure}
         with reinvestment."""
        return report


portfolio = Portfolio({
    "AAPL": 1,
    "INNT": 1,
    "GOOGL": 2,
    "FB": 3
})


if __name__ == "__main__":
    annualized_return = portfolio.annualized_return("2019-01-01", "2019-01-02")
    report = portfolio.utils.report_annualized_return(
        "2019-01-01", "2019-01-02", annualized_return)
    print(report)

    annualized_return = portfolio.annualized_return("2019-01-01", "2019-02-02")
    report = portfolio.utils.report_annualized_return(
        "2019-01-01", "2019-02-02", annualized_return)
    print(report)

    annualized_return = portfolio.annualized_return("2019-01-01", "2020-12-31")
    report = portfolio.utils.report_annualized_return(
        "2019-01-01", "2020-12-31", annualized_return)
    print(report)
