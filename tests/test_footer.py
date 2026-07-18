def test_footer_exists():
    from workshop import ui
    assert callable(ui.footer)
