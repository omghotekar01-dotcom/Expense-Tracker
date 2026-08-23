"""Unit tests for expense tracker"""

import unittest
import tempfile
import os
from datetime import datetime
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from expense_tracker.db import ExpenseDB
from expense_tracker.services import ExpenseService
from expense_tracker.models import Transaction


class TestExpenseDB(unittest.TestCase):
    def setUp(self):
        """Create temp DB for testing"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db_path = self.temp_db.name
        self.temp_db.close()
        self.db = ExpenseDB(self.db_path)
    
    def tearDown(self):
        """Clean up temp DB"""
        self.db.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
    
    def test_add_transaction(self):
        """Test adding a transaction"""
        trans = Transaction(
            id=None,
            date="2025-01-15",
            amount=50.0,
            category="Food",
            type="expense",
            notes="Lunch",
            tags="#office"
        )
        trans_id = self.db.add_transaction(trans)
        self.assertGreater(trans_id, 0)
    
    def test_get_transactions(self):
        """Test retrieving transactions"""
        trans = Transaction(
            id=None,
            date="2025-01-15",
            amount=50.0,
            category="Food",
            type="expense"
        )
        self.db.add_transaction(trans)
        
        retrieved = self.db.get_transactions()
        self.assertEqual(len(retrieved), 1)
        self.assertEqual(retrieved[0].amount, 50.0)
    
    def test_set_budget(self):
        """Test setting budget"""
        self.db.set_budget("Food", 500.0)
        budgets = self.db.get_budgets()
        self.assertEqual(budgets.get("Food"), 500.0)
    
    def test_delete_transaction(self):
        """Test deleting a transaction"""
        trans = Transaction(
            id=None,
            date="2025-01-15",
            amount=50.0,
            category="Food",
            type="expense"
        )
        trans_id = self.db.add_transaction(trans)
        
        deleted = self.db.delete_transaction(trans_id)
        self.assertTrue(deleted)
        
        retrieved = self.db.get_transactions()
        self.assertEqual(len(retrieved), 0)


class TestExpenseService(unittest.TestCase):
    def setUp(self):
        """Create temp DB and service for testing"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db_path = self.temp_db.name
        self.temp_db.close()
        self.db = ExpenseDB(self.db_path)
        self.service = ExpenseService(self.db)
    
    def tearDown(self):
        """Clean up"""
        self.db.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
    
    def test_add_expense(self):
        """Test adding an expense"""
        trans_id = self.service.add_expense("2025-01-15", 50.0, "Food", "Lunch")
        self.assertGreater(trans_id, 0)
    
    def test_add_income(self):
        """Test adding income"""
        trans_id = self.service.add_income("2025-01-15", 1000.0, "Salary", "Monthly pay")
        self.assertGreater(trans_id, 0)
    
    def test_month_summary(self):
        """Test monthly summary"""
        self.service.add_income("2025-01-15", 1000.0, "Salary")
        self.service.add_expense("2025-01-20", 50.0, "Food")
        self.service.add_expense("2025-01-25", 30.0, "Transport")
        
        summary = self.service.get_month_summary(2025, 1)
        self.assertEqual(summary['total_income'], 1000.0)
        self.assertEqual(summary['total_expense'], 80.0)
        self.assertEqual(summary['balance'], 920.0)
    
    def test_category_summary(self):
        """Test category summary"""
        self.service.add_expense("2025-01-15", 50.0, "Food")
        self.service.add_expense("2025-01-20", 30.0, "Food")
        self.service.add_expense("2025-01-25", 20.0, "Transport")
        
        cat_summary = self.service.get_category_summary()
        self.assertEqual(cat_summary.get('Food'), 80.0)
        self.assertEqual(cat_summary.get('Transport'), 20.0)
    
    def test_budget_alerts(self):
        """Test budget alert system"""
        self.db.set_budget("Food", 100.0)
        self.service.add_expense("2025-01-15", 80.0, "Food")
        
        alerts = self.service.check_budget_alerts()
        self.assertIn('Food', alerts)
        self.assertEqual(alerts['Food']['status'], 'danger')
    
    def test_prediction(self):
        """Test expense prediction"""
        self.service.add_expense("2025-01-10", 100.0, "Food")
        self.service.add_expense("2025-01-15", 150.0, "Food")
        self.service.add_expense("2025-01-20", 200.0, "Food")
        
        pred = self.service.predict_next_month_expense()
        self.assertGreater(pred, 0)


if __name__ == '__main__':
    unittest.main()
