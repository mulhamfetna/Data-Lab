import numpy as np
import pandas as pd

from workshop import visuals


def test_palette_is_five_distinct_colors():
    assert len(visuals.PALETTE) == 5
    assert len(set(visuals.PALETTE)) == 5


def test_person_svg_scales_with_value():
    thin = visuals.person_svg(0.1, "low")
    fat = visuals.person_svg(0.9, "high")
    assert "<svg" in thin and "</svg>" in thin
    # extract torso rx (the second ellipse) — wider for high value
    def rx(svg):
        import re
        return max(float(m) for m in re.findall(r'rx="([\d.]+)"', svg))
    assert rx(fat) > rx(thin)
    assert "💰" in fat and "🪙" in thin


def test_dist_overlay_returns_figure():
    rng = np.random.default_rng(0)
    real = pd.DataFrame({"age": rng.normal(40, 10, 200)})
    synth = pd.DataFrame({"age": rng.normal(40, 10, 200)})
    fig = visuals.dist_overlay(real, synth, "age", "Age")
    assert fig is not None
    assert len(fig.axes) == 1


def test_gapminder_bubble_returns_figure():
    rng = np.random.default_rng(0)
    snap = pd.DataFrame({
        "continent": ["Asia", "Europe", "Africa", "Americas", "Oceania"] * 4,
        "gdpPercap": rng.uniform(500, 40000, 20),
        "lifeExp": rng.uniform(45, 82, 20),
        "pop": rng.integers(1_000_000, 100_000_000, 20),
    })
    fig = visuals.gapminder_bubble(snap)
    assert fig is not None and len(fig.axes) == 1
