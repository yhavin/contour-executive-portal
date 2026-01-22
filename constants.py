"""
Constants and enums.

Author: Yakir Havin
"""


from enum import Enum


class IncomeStatementCategory(Enum):
    TOTAL_REVENUE = "Total Revenue"
    TOTAL_COST_OF_GOODS_SOLD = "Total Cost of Goods Sold"
    GROSS_PROFIT = "Gross Profit"
    TOTAL_OPERATING_EXPENSES = "Total Operating Expenses"
    NET_PROFIT = "Net Profit"


class Metric(Enum):
    REVENUE = "Revenue"
    GROSS_PROFIT = "Gross Profit"
    OPERATING_EXPENSES = "Operating Expenses"
    NET_PROFIT = "Net Profit"
    GROSS_PROFIT_RATIO = "Gross Profit Ratio"
    OPERATING_EXPENSE_RATIO = "Operating Expense Ratio"


METRIC_CONSTANTS = {
    Metric.REVENUE: {
        "format": {
            "axis": "$,.0f",
            "tooltip": "$,.2f"
        },
        "caption": "Total revenue earned"
    },
    Metric.GROSS_PROFIT: {
        "format": {
            "axis": "$,.0f",
            "tooltip": "$,.2f"
        },
        "caption": "Revenue minus cost of goods sold"
    },
    Metric.OPERATING_EXPENSES: {
        "format": {
            "axis": "$,.0f",
            "tooltip": "$,.2f"
        },
        "caption": "Total operating expenses"
    },
    Metric.NET_PROFIT: {
        "format": {
            "axis": "$,.0f",
            "tooltip": "$,.2f"
        },
        "caption": "Gross profit minus operating expenses"
    },
    Metric.GROSS_PROFIT_RATIO: {
        "format": {
            "axis": ".0%",
            "tooltip": ".2%"
        },
        "caption": "Gross profit divided by revenue"
    },
    Metric.OPERATING_EXPENSE_RATIO: {
        "format": {
            "axis": ".0%",
            "tooltip": ".2%"
        },
        "caption": "Operating expenses divided by revenue"
    }
}