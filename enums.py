"""
Enums.

Author: Yakir Havin
"""


from enum import Enum


class FinancialCategory(Enum):
    REVENUE = "Revenue"
    COST_OF_GOODS_SOLD = "Cost of Goods Sold"
    OPERATING_EXPENSES = "Operating Expenses"