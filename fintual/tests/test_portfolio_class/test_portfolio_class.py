from stocks.stocks import Portfolio
import pytest
import math


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
            profit = stock.amount * \
                (stock.price("2020-12-31") - stock.price("2019-01-01"))
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

    def test_get_time_between_method_integer_dates(self):
        portfolio = Portfolio({
            "AAPL": 1,
            "INNT": 1,
            "GOOGL": 2,
            "FB": 3
        })
        initial_date = "2019-01-01"
        ending_date = "2020-12-31"

        years_between_dates = portfolio.utils.get_time_between(
            initial_date, ending_date, measure="year", format="%Y-%m-%d")

        assert years_between_dates == 2

        months_between_dates = portfolio.utils.get_time_between(
            initial_date, ending_date, measure="month", format="%Y-%m-%d")

        assert months_between_dates == 24

        days_between_dates = portfolio.utils.get_time_between(
            initial_date, ending_date, measure="day", format="%Y-%m-%d")

        assert days_between_dates == 730

    def test_get_time_between_method_fraction_dates(self):
        portfolio = Portfolio({
            "AAPL": 1,
            "INNT": 1,
            "GOOGL": 2,
            "FB": 3
        })
        initial_date = "2019-01-01"
        ending_date = "2020-12-22"

        years_between_dates = portfolio.utils.get_time_between(
            initial_date, ending_date, measure="year", format="%Y-%m-%d")

        assert years_between_dates == 1.975

        months_between_dates = portfolio.utils.get_time_between(
            initial_date, ending_date, measure="month", format="%Y-%m-%d")

        assert months_between_dates == 23.704

        days_between_dates = portfolio.utils.get_time_between(
            initial_date, ending_date, measure="day", format="%Y-%m-%d")

        assert days_between_dates == 721

    def test_portfolio_annualized_return_method_success(self):
        portfolio = Portfolio({
            "AAPL": 1,
            "INNT": 1,
            "GOOGL": 2,
            "FB": 3
        })
        initial_date = "2019-01-01"
        ending_date = "2020-12-31"

        initial_investment = portfolio.sum_stock_profits(
            portfolio.get_total_stocks_prices(initial_date))

        profit = portfolio.profit(initial_date, ending_date)

        # R
        investment_return = profit/initial_investment

        # t
        years_between_dates = portfolio.utils.get_time_between(
            initial_date, ending_date, measure="year", format="%Y-%m-%d")

        # r
        theoretical_annualized_return = math.pow(
            (1 + investment_return), 1/years_between_dates) - 1

        portfolio_annualized_return = portfolio.annualized_return(
            initial_date, ending_date)


        assert theoretical_annualized_return == portfolio_annualized_return
