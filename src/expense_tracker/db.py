
import sqlite3
from typing import List, Optional
from datetime import datetime
from .models import Transaction, RecurringRule
import os
import sqlite3


class ExpenseDB:
    def __init__(self, db_path: str = "expense_tracker.db", use_sqlite_fallback: bool = True):
        self.db_path = db_path
        self.using_sqlite = True
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            amount REAL,
            category TEXT,
            type TEXT,
            notes TEXT,
            tags TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS budgets (
            category TEXT PRIMARY KEY,
            budget_limit REAL
        )''')
        conn.commit()
        conn.close()

    def add_transaction(self, trans: Transaction) -> int:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''INSERT INTO transactions (date, amount, category, type, notes, tags)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (trans.date, trans.amount, trans.category, trans.type, trans.notes, trans.tags))
        conn.commit()
        trans_id = c.lastrowid
        conn.close()
        return trans_id

    def get_transactions(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Transaction]:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        query = "SELECT id, date, amount, category, type, notes, tags FROM transactions"
        params = []
        if start_date and end_date:
            query += " WHERE date >= ? AND date < ?"
            params.extend([start_date, end_date])
        elif start_date:
            query += " WHERE date >= ?"
            params.append(start_date)
        elif end_date:
            query += " WHERE date < ?"
            params.append(end_date)
        c.execute(query, params)
        rows = c.fetchall()
        conn.close()
        transactions = [Transaction(id=row[0], date=row[1], amount=row[2], category=row[3], type=row[4], notes=row[5], tags=row[6]) for row in rows]
        return transactions

    def delete_transaction(self, trans_id: int) -> bool:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("DELETE FROM transactions WHERE id = ?", (trans_id,))
        conn.commit()
        deleted = c.rowcount > 0
        conn.close()
        return deleted

    def set_budget(self, category: str, budget_limit: float) -> bool:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO budgets (category, budget_limit) VALUES (?, ?)", (category, budget_limit))
        conn.commit()
        conn.close()
        return True

    def get_budgets(self) -> dict:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT category, budget_limit FROM budgets")
        rows = c.fetchall()
        conn.close()
        return {row[0]: row[1] for row in rows}

    # Recurring rules can be implemented as needed (e.g., in a JSON file or another table)
    def add_recurring_rule(self, rule: RecurringRule) -> int:
        # Not implemented in SQLite version
        return -1

    def get_recurring_rules(self) -> List[RecurringRule]:
        # Not implemented in SQLite version
        return []


    def update_recurring_rule(self, rule_id: int, next_date: str) -> bool:
        # Not implemented in SQLite version
        return False


    def delete_transaction(self, trans_id: int) -> bool:
        """Delete a transaction by ID"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("DELETE FROM transactions WHERE id = ?", (trans_id,))
        conn.commit()
        deleted = c.rowcount > 0
        conn.close()
        return deleted


    def set_budget(self, category: str, budget_limit: float) -> bool:
        """Set or update budget for a category"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO budgets (category, budget_limit) VALUES (?, ?)", (category, budget_limit))
        conn.commit()
        conn.close()
        return True


    def get_budgets(self) -> dict:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT category, budget_limit FROM budgets")
        rows = c.fetchall()
        conn.close()
        return {row[0]: row[1] for row in rows}

    def add_recurring_rule(self, rule: RecurringRule) -> int:
        """Add a recurring expense rule"""
        if not self.sheets:
            return -1
        
        ws = self.sheets["recurring_rules"]
        all_rows = ws.get_all_values()
        rule_id = len(all_rows)
        
        ws.append_row([
            rule_id,
            rule.transaction_id,
            rule.interval,
            rule.next_date
        ])
        return rule_id

    def get_recurring_rules(self) -> List[RecurringRule]:
        """Get all recurring expense rules"""
        if not self.sheets:
            return []
        
        ws = self.sheets["recurring_rules"]
        all_rows = ws.get_all_values()
        
        rules = []
        for row in all_rows[1:]:
            if len(row) >= 4:
                try:
                    rule = RecurringRule(
                        id=int(row[0]),
                        transaction_id=int(row[1]),
                        interval=row[2],
                        next_date=row[3]
                    )
                    rules.append(rule)
                except (ValueError, IndexError):
                    continue
        
        return rules

    def update_recurring_rule(self, rule_id: int, next_date: str) -> bool:
        """Update next date for a recurring rule"""
        if not self.sheets:
            return False
        
        ws = self.sheets["recurring_rules"]
        all_rows = ws.get_all_values()
        
        for idx, row in enumerate(all_rows[1:], start=2):
            if len(row) > 0 and int(row[0]) == rule_id:
                ws.update_cell(idx, 4, next_date)
                return True
        
        return False
    
    
