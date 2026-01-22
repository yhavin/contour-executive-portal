from datetime import datetime, timedelta

import streamlit as st
import polars as pl


# =======================
# Functions
# =======================
# @st.cache_data(show_spinner=False)
def fetch_data():
    return pl.read_csv(
        "data/trial_balance.csv",
        schema_overrides={
            "period": pl.Date,
            "gl_account_code": pl.Utf8,
            "opening_balance": pl.Float64,
            "debit": pl.Float64,
            "credit": pl.Float64,
            "closing_balance": pl.Float64,
            "activity": pl.Float64
        }
    ).sort("period")


def metrics_section(df: pl.DataFrame, period_selection: datetime):
    selected_df = df.filter(
        (pl.col("period") == period_selection) &
        (pl.col("gl_account_code").str.contains("^[4-9]"))
    )

    prior_period = (period_selection.replace(day=1) - timedelta(days=1)).replace(day=1)
    prior_df = df.filter(
        (pl.col("period") == prior_period) &
        (pl.col("gl_account_code").str.contains("^[4-9]"))
    )

    # Sum each category for selected period
    selected_total_revenue = selected_df.filter(
        pl.col("gl_account_code").str.starts_with("4")
    ).select(pl.col("activity").sum()).item() * -1

    selected_total_cost_of_goods_sold = selected_df.filter(
        pl.col("gl_account_code").str.starts_with("5")
    ).select(pl.col("activity").sum()).item()

    selected_total_operating_expenses = selected_df.filter(
        pl.col("gl_account_code").str.contains("^[6-9]")
    ).select(pl.col("activity").sum()).item()

    # Sum each category for prior period
    prior_total_revenue = prior_df.filter(
        pl.col("gl_account_code").str.starts_with("4")
    ).select(pl.col("activity").sum()).item() * -1

    prior_total_cost_of_goods_sold = prior_df.filter(
        pl.col("gl_account_code").str.starts_with("5")
    ).select(pl.col("activity").sum()).item()

    prior_total_operating_expenses = prior_df.filter(
        pl.col("gl_account_code").str.contains("^[6-9]")
    ).select(pl.col("activity").sum()).item()

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
        value=selected_total_revenue, 
        delta=total_revenue_delta, 
        format="compact",
        border=True
    )
    metric2.metric(
        label="Gross profit", 
        value=selected_total_gross_profit, 
        delta=total_gross_profit_delta,
        format="compact",
        border=True
    
    )
    metric3.metric(label="Net profit",
        value=selected_total_net_profit,
        delta=total_net_profit_delta,
        format="compact",
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
        value=selected_gross_profit_ratio * 100, 
        delta=gross_profit_ratio_delta * 100,
        format="%.1f%%",
        border=True
    )
    metric5.metric(
        label="Operating expense ratio", 
        value=selected_operating_expense_ratio * 100, 
        delta=operating_expense_ratio_delta * 100, 
        delta_color="inverse", 
        format="%.1f%%",
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