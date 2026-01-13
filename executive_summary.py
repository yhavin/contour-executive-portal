from datetime import datetime, timedelta

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
    if abs(value) >= 1000000:
        return millify(value, precision=2, drop_nulls=False)
    elif abs(value) >= 1000:
        return millify(value, precision=0)
    else:
        return str(value)


def metrics_section(df: pl.DataFrame, period_selection: datetime):
    selected_df = df.filter(pl.col("period") == period_selection)

    prior_period = (period_selection.replace(day=1) - timedelta(days=1)).replace(day=1)
    prior_df = df.filter(pl.col("period") == prior_period)

    # Sum each category for selected period
    selected_total_revenue = calculate_category_total(selected_df, FinancialCategory.REVENUE.value)
    selected_total_cost_of_goods_sold = calculate_category_total(selected_df, FinancialCategory.COST_OF_GOODS_SOLD.value)
    selected_total_operating_expenses = calculate_category_total(selected_df, FinancialCategory.OPERATING_EXPENSES.value)

    # Sum each category for prior period
    prior_total_revenue = calculate_category_total(prior_df, FinancialCategory.REVENUE.value)
    prior_total_cost_of_goods_sold = calculate_category_total(prior_df, FinancialCategory.COST_OF_GOODS_SOLD.value)
    prior_total_operating_expenses = calculate_category_total(prior_df, FinancialCategory.OPERATING_EXPENSES.value)

    # Create subtotals for selected period
    selected_total_gross_profit = selected_total_revenue - selected_total_cost_of_goods_sold
    selected_total_net_profit = selected_total_gross_profit - selected_total_operating_expenses

    # Create subtotals for prior period
    prior_total_gross_profit = prior_total_revenue - prior_total_cost_of_goods_sold
    prior_total_net_profit = prior_total_gross_profit - prior_total_operating_expenses

    # Calculate deltas
    total_revenue_delta = selected_total_revenue - prior_total_revenue
    total_gross_profit_delta = selected_total_gross_profit - prior_total_gross_profit
    total_net_profit_delta = selected_total_net_profit - prior_total_net_profit

    # Display primary metrics
    metrics_container = center.container()
    metric1, metric2, metric3 = metrics_container.columns(3)
    metric1.metric(
        label="Revenue", 
        value=f"${format_metric(selected_total_revenue)}", 
        delta=millify(total_revenue_delta), 
        border=True
    )
    metric2.metric(
        label="Gross profit", 
        value=f"${format_metric(selected_total_gross_profit)}", 
        delta=millify(total_gross_profit_delta), 
        border=True
    
    )
    metric3.metric(label="Net profit",
        value=f"${format_metric(selected_total_net_profit)}",
        delta=millify(total_net_profit_delta),
        border=True
    )

    # Calculate secondary metrics
    selected_gross_profit_ratio = selected_total_gross_profit / selected_total_revenue
    prior_gross_profit_ratio = prior_total_gross_profit / prior_total_revenue if prior_total_revenue > 0 else 0
    gross_profit_ratio_delta = selected_gross_profit_ratio - prior_gross_profit_ratio

    selected_operating_expense_ratio = selected_total_operating_expenses / selected_total_revenue
    prior_operating_expense_ratio = prior_total_operating_expenses / prior_total_revenue if prior_total_revenue > 0 else 0
    operating_expense_ratio_delta = selected_operating_expense_ratio - prior_operating_expense_ratio

    # Display secondary metrics
    metric4, metric5, metric6 = metrics_container.columns(3)
    metric4.metric(
        label="Gross profit ratio",
        value=f"{selected_gross_profit_ratio:.1%}", 
        delta=f"{gross_profit_ratio_delta:.1%}", 
        border=True
    )
    metric5.metric(
        label="Operating expense ratio", 
        value=f"{selected_operating_expense_ratio:.1%}", 
        delta=f"{operating_expense_ratio_delta:.1%}", 
        delta_color="inverse", 
        border=True
    )


# =======================
# User interface
# =======================
st.set_page_config(
    page_title="Executive summary | Executive Portal",
    layout="wide"
)
left, center, right = st.columns([1, 3.5, 1])
center.header(":material/health_metrics: Executive summary")
left_center, center_center, right_center = center.columns(3)

df = fetch_data()

period_options = df["period"].unique().to_list()
period_selection = left_center.selectbox(
    label="Period",
    options=reversed(period_options),
    index=0,
    format_func=lambda x: datetime.strftime(x, "%B %Y")
)

metrics_section(df, period_selection)