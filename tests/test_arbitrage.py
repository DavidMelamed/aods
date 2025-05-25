from aods.analytics.arbitrage import price_arbitrage_opportunities, currency_triangular_arbitrage


def test_price_arbitrage_opportunities():
    data = [
        {"item": "X", "price": 1.0, "source": "A"},
        {"item": "X", "price": 1.5, "source": "B"},
    ]
    ops = price_arbitrage_opportunities(data, "item", "price", "source")
    assert ops and ops[0]["spread"] == 0.5


def test_currency_triangular_arbitrage():
    rates = [
        {"pair": "USD/EUR", "rate": 0.9},
        {"pair": "EUR/JPY", "rate": 130.0},
        {"pair": "JPY/USD", "rate": 0.009}
    ]
    cycles = currency_triangular_arbitrage(rates)
    assert isinstance(cycles, list)
