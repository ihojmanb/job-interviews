from stocks_api.stocks_api import Stock
import pytest 

class TestStockClass:
    def test_stock_price_success(self):
        apple_stock = Stock("AAPL", 1)
        stock_price = apple_stock.price("2020-10-21")
        assert isinstance(stock_price, int)
        assert stock_price >= 0


    def test_stock_price_fail_with_no_data_for_specific_date(self):
        apple_stock = Stock("AAPL", 1)
        with pytest.raises(KeyError):
            stock_price = apple_stock.price("2023-10-21")

    def test_stock_amount_success(self):
        stock = Stock("INNT", 2)
        assert stock.amount == 2

    def test_stock_amount_fail(self):
        stock = Stock("FB", 0)
        assert not stock.amount == 2

    def test_total_stock_price(self):
        facebook_stock = Stock("FB", 2)
        stock_price = facebook_stock.price("2020-10-21")
        total_stock_price = stock_price*facebook_stock.amount
        assert isinstance(stock_price, int)
        assert total_stock_price == stock_price * 2


    def test_delta_of_stock_price_in_different_dates(self):
        google_stock =Stock("GOOGL", 100)
        buy_price = google_stock.price("2019-01-01")
        sell_price = google_stock.price("2020-03-25")
        profit = google_stock.amount*(sell_price - buy_price)
        if sell_price >= buy_price:
            assert profit >= 0
        else:
            assert profit < 0

    