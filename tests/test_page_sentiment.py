from streamlit.testing.v1 import AppTest


def test_sentiment_page_loads():
    at = AppTest.from_file("pages/63_🧪_Model_Sentiment.py", default_timeout=30).run()
    assert not at.exception
