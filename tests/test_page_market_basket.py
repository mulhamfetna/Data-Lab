from streamlit.testing.v1 import AppTest


def test_market_basket_page_loads():
    at = AppTest.from_file("pages/57_🧪_Mine_MarketBasket.py", default_timeout=30).run()
    assert not at.exception
