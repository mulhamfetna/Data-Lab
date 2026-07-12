from pathlib import Path

import pandas as pd
import streamlit as st

from workshop import ui, visuals

st.set_page_config(page_title="Public Datasets", page_icon="🧪", layout="wide")
ui.page_header(
    "🧪 Public Datasets — millions already exist, free",
    "You rarely start from zero. Governments, banks, and researchers publish huge, "
    "clean datasets. Knowing they exist turns a month of data collection into an "
    "afternoon of analysis.",
)

DATA = Path(__file__).resolve().parent.parent / "assets" / "gapminder.csv"


@st.cache_data
def load():
    return pd.read_csv(DATA)


df = load()
st.caption(f"Loaded the famous **Gapminder** dataset — {len(df):,} rows, "
           f"{df['country'].nunique()} countries, {df['year'].min()}–{df['year'].max()}.")

year = st.slider("Year", int(df["year"].min()), int(df["year"].max()),
                 int(df["year"].max()), step=5)
snap = df[df["year"] == year]

top = snap.loc[snap["lifeExp"].idxmax()]
rich = snap.loc[snap["gdpPercap"].idxmax()]
c = st.columns(3)
c[0].metric("Countries", snap["country"].nunique())
c[1].metric("Longest-lived", top["country"], f"{top['lifeExp']:.0f} yrs")
c[2].metric("Highest income", rich["country"], f"${rich['gdpPercap']:,.0f}")

st.success(f"**In {year}, {top['country']} had the highest life expectancy "
           f"({top['lifeExp']:.0f} years).** Watch how wealth and health move together — drag the "
           "year and the whole world shifts up and to the right.")

st.pyplot(visuals.gapminder_bubble(snap))
st.caption("Each dot is a country · x = income per person (log) · y = life expectancy · "
           "size = population · colour = continent.")

with st.expander("See the raw data"):
    st.dataframe(snap[["country", "continent", "lifeExp", "pop", "gdpPercap"]]
                 .sort_values("lifeExp", ascending=False), use_container_width=True)
