"""Recurring expenses management"""

from datetime import datetime, timedelta
from typing import List, Optional
from .db import ExpenseDB
from .models import Transaction
import json


class RecurringExpenseManager:
    def __init__(self, db: ExpenseDB):
        self.db = db
    
    def create_recurring_expense(self, date: str, amount: float, category: str, 
                                interval: str = "monthly", notes: str = "", tags: str = "") -> tuple:
        """
        Create a recurring expense
        interval: 'weekly', 'monthly', 'yearly'
        Returns: (transaction_id, recurring_rule_id)
        """
        # Add initial transaction
        trans = Transaction(
            id=None,
            date=date,
            amount=amount,
            category=category,
            type="expense",
            notes=notes,
            tags=tags
        )
        trans_id = self.db.add_transaction(trans)
        
        # Calculate next date
        date_obj = datetime.fromisoformat(date)
        if interval == "weekly":
            next_date = (date_obj + timedelta(weeks=1)).isoformat()
        elif interval == "monthly":
            if date_obj.month == 12:
                next_date = date_obj.replace(year=date_obj.year + 1, month=1).isoformat()
            else:
                next_date = date_obj.replace(month=date_obj.month + 1).isoformat()
        elif interval == "yearly":
            next_date = date_obj.replace(year=date_obj.year + 1).isoformat()
        else:
            return (trans_id, None)
        
        # Add recurring rule (we'll use JSON in a file since we don't have a recurring table)
        rule = {
            "transaction_id": trans_id,
            "interval": interval,
            "next_date": next_date,
            "original_amount": amount,
            "original_category": category,
            "original_notes": notes,
            "original_tags": tags
        }
        
        return (trans_id, rule)
    
    def process_recurring_expenses(self, recurring_rules: List[dict], today: Optional[str] = None) -> List[int]:
        """
        Process all recurring expenses that are due today
        Returns list of newly created transaction IDs
        """
        if today is None:
            today = datetime.now().isoformat()[:10]
        
        new_trans_ids = []
        
        for rule in recurring_rules:
            if rule['next_date'] <= today:
                # Create new transaction
                trans = Transaction(
                    id=None,
                    date=today,
                    amount=rule['original_amount'],
                    category=rule['original_category'],
                    type="expense",
                    notes=rule['original_notes'],
                    tags=rule['original_tags']
                )
                trans_id = self.db.add_transaction(trans)
                new_trans_ids.append(trans_id)
                
                # Update next date
                date_obj = datetime.fromisoformat(rule['next_date'])
                if rule['interval'] == "weekly":
                    rule['next_date'] = (date_obj + timedelta(weeks=1)).isoformat()
                elif rule['interval'] == "monthly":
                    if date_obj.month == 12:
                        rule['next_date'] = date_obj.replace(year=date_obj.year + 1, month=1).isoformat()
                    else:
                        rule['next_date'] = date_obj.replace(month=date_obj.month + 1).isoformat()
                elif rule['interval'] == "yearly":
                    rule['next_date'] = date_obj.replace(year=date_obj.year + 1).isoformat()
        
        return new_trans_ids
