from aods.analytics.arbitrage import price_arbitrage_opportunities


def test_price_arbitrage_opportunities():
    data = [
        {"item": "X", "price": 1.0, "source": "A"},
        {"item": "X", "price": 1.5, "source": "B"},
    ]
    ops = price_arbitrage_opportunities(data, "item", "price", "source")
    assert ops and ops[0]["spread"] == 0.5
