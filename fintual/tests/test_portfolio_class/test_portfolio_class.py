from stocks.stocks import Portfolio
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


    def test_portfolio_profit_method_success(self):
        portfolio = Portfolio({
            "AAPL": 100,
            "INNT": 50,
            "GOOGL": 2,
            "FB": 300
        })
        portfolio_profit = portfolio.profit("2019-01-01", "2020-12-31")
        theoretical_profit = 0
        for stock in portfolio.stocks:
            profit = stock.amount * (stock.price("2020-12-31")- stock.price("2019-01-01"))
            theoretical_profit += profit
        assert portfolio_profit == theoretical_profit


    def test_portfolio_profit_method_success_fail(self):
        portfolio = Portfolio({
            "AAPL": 100,
            "INNT": 50,
            "GOOGL": 2,
            "FB": 300
        })
        with pytest.raises(KeyError):
            portfolio_profit = portfolio.profit("2025-01-01", "2020-12-31")


    def test_portfolio_profit_method_fails_with_non_existent_ticker(self):
        portfolio = Portfolio({
            "AAPL": 100, 
            "XOM": 50,
            "GE": 2,
            "MSFT": 300
        })
        with pytest.raises(KeyError):
            portfolio_profit = portfolio.profit("2019-01-01", "2020-12-31")