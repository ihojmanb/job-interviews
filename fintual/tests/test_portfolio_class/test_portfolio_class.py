from stocks_api.stocks_api import Portfolio
import pytest

class TestPortfolioClass:
    
    def test_portfolio_stock_collection_is_not_empty(self):
        portfolio = Portfolio({
            "AAPL": 100,
            "INNT": 50,
            "GOOGL": 2,
            "FB": 300
        })
        assert len(portfolio.stocks) > 0
        assert isinstance(portfolio.stocks, list)

    def test_portfolio_stock_collection_is_empty(self):
        portfolio = Portfolio({})
        assert len(portfolio.stocks) == 0


    def test_portfolio_profit_method(self):
        portfolio = Portfolio({
            "AAPL": 100,
            "INNT": 50,
            "GOOGL": 2,
            "FB": 300
        })
        portfolio_profit = portfolio.profit("2019-01-01", "2020-12-31")
        assert isinstance(portfolio_profit, int)


    def test_portfolio_profit_method_fails_with_non_existent_ticker(self):
        portfolio = Portfolio({
            "AAPL": 100, 
            "XOM": 50,
            "GE": 2,
            "MSFT": 300
        })
        with pytest.raises(ValueError):
            portfolio_profit = portfolio.profit("2019-01-01", "2020-12-31")