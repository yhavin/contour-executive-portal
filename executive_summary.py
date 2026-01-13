from datetime import datetime

import streamlit as st
import polars as pl
from millify import millify

from enums import FinancialCategory


# =======================
# Functions
# =======================
# @st.cache_data(show_spinner=False)
def fetch_data():
    return pl.read_csv(
        "data/high_level_financial_summary.csv",
        schema_overrides={"period": pl.Date}
    ).sort("period")


def calculate_category_total(df: pl.DataFrame, category: str, value_column: str="activity"):
    """SUMIF on a DataFrame (category is case-insensitive)."""
    return df.filter(pl.col("category").str.to_lowercase() == category.lower()).select(pl.col(value_column).sum()).item()


def format_metric(value) -> str:
    if value >= 1000000:
        return millify(value, precision=2, drop_nulls=False)
    elif value >= 1000:
        return millify(value, precision=0)
    else:
        return str(value)


def metrics_section(df: pl.DataFrame, from_period_selection: datetime, to_period_selection: datetime):
    df = df.filter((pl.col("period") >= from_period_selection) & (pl.col("period") <= to_period_selection))

    # Sum each category
    total_revenue = calculate_category_total(df, FinancialCategory.REVENUE.value)
    total_cost_of_goods_sold = calculate_category_total(df, FinancialCategory.COST_OF_GOODS_SOLD.value)
    total_operating_expenses = calculate_category_total(df, FinancialCategory.OPERATING_EXPENSES.value)

    # Create subtotals
    total_gross_profit = total_revenue - total_cost_of_goods_sold
    total_net_profit = total_gross_profit - total_operating_expenses

    metrics_container = center.container(border=True, horizontal=True)
    col1, col2, col3 = metrics_container.columns(3)
    col1.metric(label="Revenue", value=f"${format_metric(total_revenue)}")
    col2.metric(label="Gross Profit", value=f"${format_metric(total_gross_profit)}")
    col3.metric(label="Net Profit", value=f"${format_metric(total_net_profit)}")



# =======================
# User interface
# =======================
st.set_page_config(
    page_title="Executive summary | Executive Portal",
    layout="wide"
)
left, center, right = st.columns([1, 5, 1])
center.header(":material/dashboard: Executive summary")
left_center, center_center, right_center = center.columns(3)

df = fetch_data()

period_options = df["period"].unique().to_list()
from_period_selection, to_period_selection = left_center.select_slider(
    label="Date range",
    options=period_options,
    value=(period_options[0], period_options[-1]),
    format_func=lambda x: datetime.strftime(x, "%B %Y")
)

metrics_section(df, from_period_selection, to_period_selection)
