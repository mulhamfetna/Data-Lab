from pathlib import Path

from workshop import tracks

ROOT = Path(__file__).resolve().parents[1]


def test_four_roles_each_with_demos():
    assert len(tracks.roles()) == 4
    for role in tracks.roles():
        t = tracks.track(role)
        assert t["icon"] and t["blurb"]
        assert len(t["demos"]) >= 5


def test_every_linked_page_file_exists():
    for file in tracks.all_demo_files():
        assert (ROOT / file).exists(), f"missing page: {file}"


def test_demo_entries_are_well_formed():
    for role in tracks.roles():
        for file, title, why in tracks.track(role)["demos"]:
            assert file.startswith("pages/") and title and why
