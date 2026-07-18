from streamlit.testing.v1 import AppTest


def test_embeddings_page_loads():
    at = AppTest.from_file("pages/54_🧪_Encode_Embeddings.py", default_timeout=30).run()
    assert not at.exception
