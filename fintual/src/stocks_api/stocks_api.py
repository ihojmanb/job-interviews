import json
from functools import reduce

stocks_data = open("fake_data.json")
stocks_data = json.load(stocks_data)
available_tickers = [stock["ticker"] for stock in stocks_data]


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

# TODO Refactor!!!!!!
# es feo que esté llamando a una variable global,
# debería ser independiente de eso

    def price(self, date: str):
        if self.symbol in available_tickers:
            stock_data = [
                stock for stock in stocks_data if stock["ticker"] == self.symbol]
            stock_price = stock_data[0]["prices"][date]
            return stock_price
        else:
            raise ValueError("ticker is not in our database.")


class Portfolio:
    def __init__(self, stock_collection: dict) -> None:
        self._stocks = self.set_stock_collection(stock_collection)

    @property
    def stocks(self):
        return self._stocks

    def set_stock_collection(self, stock_dict):
        stock_collection = []
        for symbol, amount in stock_dict.items():
            stock_collection.append(Stock(symbol, amount))
        return stock_collection

    def get_stocks_prices(self, date):
        stocks_prices = list(map(lambda stock: stock.price(date), self.stocks))
        return stocks_prices

    def get_stocks_amount(self):
        return list(map(lambda stock: stock.amount, self.stocks))

    def multiply_stock_prices_by_amounts(self, stocks_buy_prices, stocks_amount):
        return [a*b for a, b in zip(stocks_buy_prices, stocks_amount)]

    def substract_buy_to_sell_prices(self,
                                     list_of_total_stocks_buy_prices, list_of_total_stocks_sell_prices):
        return [a-b for a, b in zip(list_of_total_stocks_sell_prices, list_of_total_stocks_buy_prices)]

    # TODO Refactor!!!!!
    # podemos dividir este código en subrutinas

    def profit(self, init_date, end_date):
        list_of_stocks_amount = self.get_stocks_amount()
        list_of_stocks_buy_prices = self.get_stocks_prices(init_date)
        list_of_stocks_sell_prices = self.get_stocks_prices(end_date)
        list_of_total_stocks_buy_prices = self.multiply_stock_prices_by_amounts(
            list_of_stocks_buy_prices, list_of_stocks_amount)
        # print(list_of_total_stocks_buy_prices)
        list_of_total_stocks_sell_prices = self.multiply_stock_prices_by_amounts(
            list_of_stocks_sell_prices, list_of_stocks_amount)
        # print(list_of_total_stocks_sell_prices)
        list_of_profit_by_stock = self.substract_buy_to_sell_prices(
            list_of_total_stocks_buy_prices, list_of_total_stocks_sell_prices)
        # print(list_of_profit_by_stock)
        profit = reduce(lambda x, y: x + y, list_of_profit_by_stock)
        return profit


portfolio = Portfolio({
    "AAPL": 100,
    "INNT": 50,
    "GOOGL": 2,
    "FB": 300
})
portfolio_profit = portfolio.profit("2020-02-11", "2020-11-03")
print(portfolio_profit)
