from workshop import geospatial as geo, store_data as sd


def _df():
    return sd.clean_orders(sd.messy_orders())


def test_city_volumes_has_coords_and_is_sorted():
    vols = geo.city_volumes(_df())
    assert set(["city", "orders", "revenue", "lat", "lon"]).issubset(vols.columns)
    assert vols["orders"].is_monotonic_decreasing
    # every mapped city is a known coordinate
    assert set(vols["city"]).issubset(set(geo.CITY_COORDS))


def test_coords_are_within_syria_bounds():
    for lat, lon in geo.CITY_COORDS.values():
        assert 32 < lat < 38 and 35 < lon < 43


def test_top_city_matches_highest_orders():
    vols = geo.city_volumes(_df())
    assert geo.top_city(_df()) == vols.iloc[0]["city"]


def test_unknown_cities_are_dropped():
    df = _df()
    df.loc[df.index[:5], "city"] = "Atlantis"
    vols = geo.city_volumes(df)
    assert "Atlantis" not in set(vols["city"])
