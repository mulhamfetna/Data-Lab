from streamlit.testing.v1 import AppTest


def test_montecarlo_page_loads():
    at = AppTest.from_file("pages/95_🧪_Adv_MonteCarlo.py", default_timeout=30).run()
    assert not at.exception
