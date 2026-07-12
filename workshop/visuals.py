"""Reusable, self-contained visuals: a validated palette, styled figures, and SVG art.

Palette is the Okabe-Ito colourblind-safe set (validated: worst adjacent ΔE ~36).
No external images — everything is generated so the app runs fully offline.
"""
import io

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Okabe-Ito categorical palette (fixed order, never cycled).
PALETTE = ["#0072B2", "#E69F00", "#009E73", "#D55E00", "#CC79A7"]
REAL, SYNTH = PALETTE[0], PALETTE[1]
INK, MUTED = "#22262b", "#8a9098"


def _style(ax):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.grid(axis="y", color="#e6e6e3", linewidth=0.8)
    ax.set_axisbelow(True)
    return ax


def dist_overlay(real, synth, column: str, label: str):
    """Overlay real vs synthetic distributions for one column (utility check, visual)."""
    fig, ax = plt.subplots(figsize=(5, 3), dpi=120)
    ax.hist(real[column], bins=30, color=REAL, alpha=0.55, label="real", density=True)
    ax.hist(synth[column], bins=30, color=SYNTH, alpha=0.55, label="synthetic", density=True)
    ax.set_title(f"{label}: real vs synthetic", color=INK, fontsize=11)
    ax.set_xlabel(label, color=MUTED, fontsize=9)
    ax.legend(frameon=False, fontsize=9)
    _style(ax)
    fig.tight_layout()
    return fig


CONTINENT_COLORS = {"Asia": PALETTE[0], "Europe": PALETTE[1], "Africa": PALETTE[2],
                    "Americas": PALETTE[3], "Oceania": PALETTE[4]}


def gapminder_bubble(snap):
    """The iconic income-vs-lifespan bubble chart, one dot per country, sized by population."""
    fig, ax = plt.subplots(figsize=(6.5, 4), dpi=120)
    for cont, color in CONTINENT_COLORS.items():
        sub = snap[snap["continent"] == cont]
        ax.scatter(sub["gdpPercap"], sub["lifeExp"], s=sub["pop"] / 200000,
                   c=color, alpha=0.75, edgecolors="white", linewidths=0.5, label=cont)
    ax.set_xscale("log")
    ax.set_xlabel("Income per person (GDP per capita, log scale)", color=MUTED, fontsize=9)
    ax.set_ylabel("Life expectancy (years)", color=MUTED, fontsize=9)
    ax.legend(frameon=False, fontsize=8, loc="lower right", title="Continent")
    _style(ax)
    fig.tight_layout()
    return fig


def person_svg(value: float, caption: str = "") -> str:
    """A little figure whose body scales with value: thin+grey (low) → wide+green (high)."""
    v = max(0.0, min(1.0, value))
    torso_rx = 16 + v * 34            # 16 (thin) .. 50 (wide)
    color = "#009E73" if v >= 0.5 else "#9aa0a6"
    skin = "#f1c27d"
    coin = "💰" if v >= 0.5 else "🪙"
    return f"""
<svg width="200" height="250" viewBox="0 0 200 250" xmlns="http://www.w3.org/2000/svg" role="img">
  <ellipse cx="100" cy="210" rx="{torso_rx+18}" ry="10" fill="#00000010"/>
  <circle cx="100" cy="46" r="24" fill="{skin}"/>
  <ellipse cx="100" cy="135" rx="{torso_rx}" ry="62" fill="{color}"/>
  <rect x="{100-10}" y="188" width="8" height="46" rx="4" fill="{color}"/>
  <rect x="{100+2}" y="188" width="8" height="46" rx="4" fill="{color}"/>
  <text x="100" y="30" text-anchor="middle" font-size="22">{coin}</text>
  <text x="100" y="247" text-anchor="middle" font-size="13" fill="#22262b"
        font-family="sans-serif" font-weight="700">{caption}</text>
</svg>"""


def fig_to_note(fig) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    return buf.getvalue()
