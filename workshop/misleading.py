"""Same numbers, opposite story — how a truncated axis manufactures drama."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from workshop.visuals import PALETTE, _style


def series() -> pd.DataFrame:
    return pd.DataFrame({"month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
                         "value": [100, 101, 101, 102, 103, 104]})


def bar_fig(df: pd.DataFrame, truncate: bool):
    fig, ax = plt.subplots(figsize=(5, 3), dpi=120)
    ax.bar(df["month"], df["value"], color=PALETTE[0], width=0.6)
    if truncate:
        ax.set_ylim(99, df["value"].max() + 0.5)
    else:
        ax.set_ylim(0, df["value"].max() * 1.15)
    _style(ax)
    fig.tight_layout()
    return fig
