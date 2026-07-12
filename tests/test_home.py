from streamlit.testing.v1 import AppTest


def test_home_loads_and_shows_lifecycle():
    at = AppTest.from_file("Home.py").run()
    assert not at.exception
    body = " ".join(m.value for m in at.markdown)
    assert "Collect" in body and "Decision" in body
