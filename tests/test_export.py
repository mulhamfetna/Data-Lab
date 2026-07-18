import io
import zipfile

from workshop import export


def test_bundle_is_a_zip_with_expected_files():
    data = export.bundle()
    z = zipfile.ZipFile(io.BytesIO(data))
    names = z.namelist()
    assert "nour_store_report.txt" in names
    assert "nour_store_clean.csv" in names
    assert z.read("nour_store_report.txt").startswith(b"Nour Store")
