from workshop import quantize as qz


def test_quantize_reduces_colors():
    img = qz.make_demo_image()
    orig = qz.unique_colors(img)
    q = qz.quantize_image(img, 8)
    assert qz.unique_colors(q) <= 8
    assert orig > 8


def test_binning_produces_requested_bins():
    import pandas as pd
    s = pd.Series(range(100))
    out = qz.bin_series(s, 5)
    assert len(out) == 5
    assert out.sum() == 100
