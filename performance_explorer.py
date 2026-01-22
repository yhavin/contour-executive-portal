from datetime import datetime

import streamlit as st
import polars as pl
import altair as alt

from constants import Metric, METRIC_CONSTANTS


# =======================
# Functions
# =======================
# @st.cache_data(show_spinner=False)
def fetch_data():
    return pl.read_csv(
        "data/performance_metrics.csv",
        schema_overrides={"period": pl.Date}
    ).sort("period")


def performance_explorer_section(df: pl.DataFrame, metric_selection: Metric, from_period_selection: datetime, to_period_selection: datetime):
    df = df.filter(pl.col("metric").str.to_lowercase() == metric_selection.value.lower())
    df = df.filter(pl.col("period").is_between(from_period_selection, to_period_selection))
    
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X(
            "yearmonth(period):T",
            title=None,
            axis=alt.Axis(
                format="%B %Y",
                labelAngle=-45,
                labelAlign="right",
                labelOverlap=False
            ),
        ),
        y=alt.Y(
            "value:Q",
            title=None,
            axis=alt.Axis(format=METRIC_CONSTANTS[metric_selection]["format"]["axis"])
        ),
        tooltip=[
            alt.Tooltip("period:T", title="Period", format="%B %Y"),
            alt.Tooltip("value:Q", title=metric_selection.value, format=METRIC_CONSTANTS[metric_selection]["format"]["tooltip"])
        ]
    )

    with center.container(border=True):
        st.altair_chart(chart)


# =======================
# User interface
# =======================
st.set_page_config(
    page_title="Performance explorer | Executive Portal",
    layout="wide"
)
left, center, right = st.columns([1, 5, 1])
center.header(":material/explore: Performance explorer")
left_center, center_center, right_center = center.columns(3)

df = fetch_data()

period_options = df["period"].unique().to_list()
from_period_selection, to_period_selection = left_center.select_slider(
    label="Date range",
    options=(period_options),
    value=(period_options[0], period_options[-1]),
    format_func=lambda x: datetime.strftime(x, "%B %Y")
)

metric_selection = left_center.selectbox(
    label="Metric",
    options=list(Metric),
    format_func=lambda x: x.value
)
left_center.caption(body=METRIC_CONSTANTS[metric_selection]["caption"])

performance_explorer_section(df, metric_selection, from_period_selection, to_period_selection)