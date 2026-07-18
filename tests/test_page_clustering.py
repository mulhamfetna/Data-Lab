from streamlit.testing.v1 import AppTest


def test_clustering_page_loads():
    at = AppTest.from_file("pages/58_🧪_Mine_Clustering.py", default_timeout=30).run()
    assert not at.exception
