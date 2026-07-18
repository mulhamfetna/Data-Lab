from workshop import misleading as ms


def test_series_and_figs():
    df = ms.series()
    assert len(df) == 6
    fig_t = ms.bar_fig(df, truncate=True)
    fig_h = ms.bar_fig(df, truncate=False)
    assert fig_t.axes[0].get_ylim()[0] >= 99      # truncated axis starts high
    assert fig_h.axes[0].get_ylim()[0] == 0       # honest axis starts at zero
