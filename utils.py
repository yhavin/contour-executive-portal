"""
Utility functions.

Author: Yakir Havin
"""


import polars as pl
from millify import millify


def calculate_category_total(df: pl.DataFrame, category: str, value_column: str="activity"):
    """SUMIF on a DataFrame (category is case-insensitive)."""
    return df.filter(pl.col("category").str.to_lowercase() == category.lower()).select(pl.col(value_column).sum()).item()


def format_metric(value) -> str:
    "Apply millify logic with conditions."
    if abs(value) >= 1000000:
        return millify(value, precision=2, drop_nulls=False)
    elif abs(value) >= 1000:
        return millify(value, precision=0)
    else:
        return str(value)