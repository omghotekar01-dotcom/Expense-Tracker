"""Business logic for expense tracking"""

import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from .db import ExpenseDB
from .models import Transaction


class ExpenseService:
    def __init__(self, db: ExpenseDB):
        self.db = db

    def add_expense(self, date: str, amount: float, category: str, notes: str = "", tags: str = "") -> int:
        """Add an expense"""
        trans = Transaction(
            id=None,
            date=date,
            amount=amount,
            category=category,
            type="expense",
            notes=notes,
            tags=tags
        )
        return self.db.add_transaction(trans)

    def add_income(self, date: str, amount: float, source: str, notes: str = "") -> int:
        """Add an income entry"""
        trans = Transaction(
            id=None,
            date=date,
            amount=amount,
            category=source,
            type="income",
            notes=notes,
            tags=None
        )
        return self.db.add_transaction(trans)

    def get_month_summary(self, year: int, month: int) -> Dict:
        """Get expense and income summary for a given month"""
        start_date = f"{year:04d}-{month:02d}-01"
        if month == 12:
            end_date = f"{year+1:04d}-01-01"
        else:
            end_date = f"{year:04d}-{month+1:02d}-01"
        
        trans = self.db.get_transactions(start_date, end_date)
        
        expenses = [t for t in trans if t.type == "expense"]
        income = [t for t in trans if t.type == "income"]
        
        total_expense = sum(t.amount for t in expenses)
        total_income = sum(t.amount for t in income)
        balance = total_income - total_expense
        
        by_category = {}
        for t in expenses:
            if t.category not in by_category:
                by_category[t.category] = 0
            by_category[t.category] += t.amount
        
        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance,
            "by_category": by_category,
            "count": len(expenses)
        }

    def get_category_summary(self) -> Dict[str, float]:
        """Get total expense by category (all time)"""
        trans = self.db.get_transactions()
        expenses = [t for t in trans if t.type == "expense"]
        by_category = {}
        for t in expenses:
            if t.category not in by_category:
                by_category[t.category] = 0
            by_category[t.category] += t.amount
        return by_category

    def check_budget_alerts(self) -> Dict[str, Dict]:
        """Check if any categories exceed budget limits and return alert levels"""
        budgets = self.db.get_budgets()
        category_sums = self.get_category_summary()
        alerts = {}
        
        for category, limit in budgets.items():
            spent = category_sums.get(category, 0)
            percent = (spent / limit * 100) if limit > 0 else 0
            
            if percent >= 100:
                status = "exceeded"
            elif percent >= 80:
                status = "danger"
            elif percent >= 50:
                status = "warning"
            else:
                status = "ok"
            
            alerts[category] = {
                "spent": spent,
                "limit": limit,
                "percent": percent,
                "status": status
            }
        
        return alerts

    def search_transactions(self, query: str, category: Optional[str] = None, 
                          min_amount: Optional[float] = None, 
                          max_amount: Optional[float] = None) -> List[Transaction]:
        """Search transactions by text and filters"""
        trans = self.db.get_transactions()
        
        results = []
        for t in trans:
            # Text search in notes and tags
            if query.lower() not in (t.notes or "").lower() and query.lower() not in (t.tags or "").lower():
                if query and str(query) not in str(t.amount):
                    continue
            
            # Category filter
            if category and t.category != category:
                continue
            
            # Amount range
            if min_amount and t.amount < min_amount:
                continue
            if max_amount and t.amount > max_amount:
                continue
            
            results.append(t)
        
        return results

    def get_sorted_transactions(self, sort_by: str = "date", ascending: bool = False) -> List[Transaction]:
        """Get transactions sorted by field"""
        trans = self.db.get_transactions()
        
        if sort_by == "date":
            trans.sort(key=lambda x: x.date, reverse=not ascending)
        elif sort_by == "amount":
            trans.sort(key=lambda x: x.amount, reverse=not ascending)
        elif sort_by == "category":
            trans.sort(key=lambda x: x.category, reverse=not ascending)
        
        return trans

    def predict_next_month_expense(self, months: int = 3) -> float:
        """Predict next month's expense using average of last N months"""
        trans = self.db.get_transactions()
        expenses = [t.amount for t in trans if t.type == "expense"]
        
        if not expenses:
            return 0.0
        
        # Simple average prediction
        avg = np.mean(expenses) if expenses else 0
        return float(avg)

    def get_savings_recommendation(self, target_savings_percent: float = 20.0) -> Dict:
        """Suggest how much to save based on income and expenses"""
        trans = self.db.get_transactions()
        income_list = [t.amount for t in trans if t.type == "income"]
        expense_list = [t.amount for t in trans if t.type == "expense"]
        
        total_income = sum(income_list) if income_list else 0
        total_expense = sum(expense_list) if expense_list else 0
        
        recommended_savings = total_income * (target_savings_percent / 100)
        current_balance = total_income - total_expense
        
        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "current_balance": current_balance,
            "recommended_savings": recommended_savings,
            "can_achieve": current_balance >= recommended_savings
        }

    def export_to_csv(self, filepath: str) -> bool:
        """Export transactions to CSV"""
        try:
            import csv
            trans = self.db.get_transactions()
            with open(filepath, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Date', 'Amount', 'Category', 'Type', 'Notes', 'Tags'])
                for t in trans:
                    # Format date as YYYY-MM-DD for clarity
                    date_str = t.date[:10] if t.date else ''
                    writer.writerow([date_str, t.amount, t.category, t.type, t.notes or '', t.tags or ''])
            return True
        except Exception as e:
            print(f"Error exporting CSV: {e}")
            return False

    def export_to_txt(self, filepath: str) -> bool:
        """Export transactions to TXT"""
        try:
            trans = self.db.get_transactions()
            
            with open(filepath, 'w') as f:
                f.write("EXPENSE TRACKER REPORT\n")
                f.write("=" * 50 + "\n\n")
                
                for t in trans:
                    f.write(f"Date: {t.date}\n")
                    f.write(f"Type: {t.type.upper()}\n")
                    f.write(f"Category: {t.category}\n")
                    f.write(f"Amount: {t.amount}\n")
                    if t.notes:
                        f.write(f"Notes: {t.notes}\n")
                    if t.tags:
                        f.write(f"Tags: {t.tags}\n")
                    f.write("-" * 50 + "\n\n")
            
            return True
        except Exception as e:
            print(f"Error exporting TXT: {e}")
            return False
