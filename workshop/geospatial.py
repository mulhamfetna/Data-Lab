"""Geospatial — put the business on a map, because *where* is a decision variable.

A table of orders-by-city is fine; a map is a briefing. Seeing demand cluster in one region
tells a leader where to open a hub, run a promotion, or add delivery capacity — questions a
spreadsheet buries. Here we roll Nour Store's orders up to its five Syrian cities and place
them on the map by real coordinates.
"""
from __future__ import annotations

import pandas as pd

# Approximate coordinates of the cities used in the store data.
CITY_COORDS: dict[str, tuple[float, float]] = {
    "Aleppo": (36.2021, 37.1343),
    "Damascus": (33.5138, 36.2765),
    "Homs": (34.7324, 36.7137),
    "Latakia": (35.5196, 35.7915),
    "Hama": (35.1318, 36.7578),
}


def city_volumes(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate orders and revenue per city, with lat/lon attached.

    Only cities we have coordinates for are kept (others can't be mapped). Returns columns
    ``city, orders, revenue, lat, lon`` sorted by orders descending.
    """
    grouped = df.groupby("city").agg(orders=("order_id", "count"),
                                     revenue=("amount", "sum")).reset_index()
    grouped = grouped[grouped["city"].isin(CITY_COORDS)].copy()
    grouped["lat"] = grouped["city"].map(lambda c: CITY_COORDS[c][0])
    grouped["lon"] = grouped["city"].map(lambda c: CITY_COORDS[c][1])
    grouped["revenue"] = grouped["revenue"].round(2)
    return grouped.sort_values("orders", ascending=False).reset_index(drop=True)


def top_city(df: pd.DataFrame) -> str:
    """The city with the most orders — the headline of the map."""
    vols = city_volumes(df)
    return str(vols.iloc[0]["city"]) if len(vols) else ""
