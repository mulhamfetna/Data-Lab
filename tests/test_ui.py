def test_ui_functions_exist():
    from workshop import ui
    assert callable(ui.page_header)
    assert callable(ui.leader_takeaway)
