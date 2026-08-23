"""Expense tracker package"""
from .db import ExpenseDB
from .models import Transaction, RecurringRule
from .services import ExpenseService
from .recurring import RecurringExpenseManager

from expense_tracker.db import create_table

create_table()


__all__ = ['ExpenseDB', 'Transaction', 'RecurringRule', 'ExpenseService', 'RecurringExpenseManager']
