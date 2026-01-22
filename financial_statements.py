from datetime import datetime

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
            "opening_balance": pl.Float64,
            "debit": pl.Float64,
            "credit": pl.Float64,
            "closing_balance": pl.Float64,
            "activity": pl.Float64
        }
    ).sort("period")


def income_statement_section(df: pl.DataFrame, from_period_selection: datetime, to_period_selection: datetime):
    pass


def balance_sheet_section(df: pl.DataFrame, from_period_selection: datetime, to_period_selection: datetime):
    pass


def cash_flow_statement_section(df: pl.DataFrame, from_period_selection: datetime, to_period_selection: datetime):
    pass


# =======================
# User interface
# =======================
st.set_page_config(
    page_title="Financial statements | Executive Portal",
    layout="wide"
)

left, center, right = st.columns([1, 7, 1])
center.header(":material/article: Financial statements")

df = fetch_data()

financial_statement_selection = center.pills(
    label="Statement type",
    options=["Income Statement", "Balance Sheet", "Cash Flow Statement"],
    default="Income Statement"
)

left_center, center_center, right_center = center.columns(3)

period_options = df["period"].unique().to_list()
from_period_selection, to_period_selection = left_center.select_slider(
    label="Date range",
    options=(period_options),
    value=(period_options[0], period_options[-1]),
    format_func=lambda x: datetime.strftime(x, "%B %Y")
)

if financial_statement_selection == "Income Statement":
    income_statement_section(df, from_period_selection, to_period_selection)
elif financial_statement_selection == "Balance Sheet":
    balance_sheet_section(df, from_period_selection, to_period_selection)
elif financial_statement_selection == "Cash Flow Statement":
    cash_flow_statement_section(df, from_period_selection, to_period_selection)