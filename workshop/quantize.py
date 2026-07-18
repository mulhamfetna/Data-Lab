"""Quantization: shrink data by using fewer distinct values — colors, bins, or precision."""
import io

import numpy as np
import pandas as pd
from PIL import Image


def make_demo_image(w: int = 260, h: int = 170) -> Image.Image:
    x = np.linspace(0, 1, w)
    y = np.linspace(0, 1, h)
    xx, yy = np.meshgrid(x, y)
    r = np.sin(xx * 6) * 0.5 + 0.5
    g = np.cos(yy * 6) * 0.5 + 0.5
    b = (xx + yy) / 2
    arr = (np.stack([r, g, b], axis=-1) * 255).astype("uint8")
    return Image.fromarray(arr, "RGB")


def quantize_image(img: Image.Image, n_colors: int) -> Image.Image:
    return img.convert("RGB").quantize(colors=n_colors).convert("RGB")


def unique_colors(img: Image.Image) -> int:
    return len(set(img.getdata()))


def png_bytes(img: Image.Image) -> int:
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return len(buf.getvalue())


def bin_series(s: pd.Series, bins: int) -> pd.Series:
    counts = pd.cut(s, bins=bins).value_counts(sort=False)
    counts.index = counts.index.astype(str)   # Interval → str (chart-friendly)
    return counts
