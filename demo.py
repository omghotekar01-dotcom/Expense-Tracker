#!/usr/bin/env python
"""Demo script showing all features of the expense tracker"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from expense_tracker.db import ExpenseDB
from expense_tracker.services import ExpenseService
from expense_tracker.recurring import RecurringExpenseManager
from datetime import datetime, timedelta

print("\n" + "="*60)
print("SMART EXPENSE TRACKER & BUDGET ANALYZER - DEMO")
print("="*60 + "\n")

# Initialize with Google Sheets
db = ExpenseDB("Expense Tracker Demo")
service = ExpenseService(db)
recurring_mgr = RecurringExpenseManager(db)

if not db.sheets:
    print("ERROR: Google Sheets not connected.")
    print("Please set up credentials first: read GOOGLE_SHEETS_SETUP.md")
    sys.exit(1)

print("1. ADDING SAMPLE DATA")
print("-" * 60)

# Add income
print("\n[+] Adding Income:")
income_id = service.add_income("2025-01-01", 5000, "Salary", "Monthly salary")
print(f"  OK Salary added (ID: {income_id})")

# Add expenses
expenses_data = [
    ("2025-01-05", 50, "Food", "Groceries", "#weekly"),
    ("2025-01-08", 30, "Transport", "Cab fare", "#daily"),
    ("2025-01-10", 200, "Shopping", "Clothes", "#personal"),
    ("2025-01-12", 45, "Entertainment", "Movie ticket", "#weekend"),
    ("2025-01-15", 100, "Food", "Restaurant", "#social"),
    ("2025-01-18", 500, "Utilities", "Electricity bill", "#monthly"),
    ("2025-01-20", 35, "Transport", "Bus pass", "#daily"),
    ("2025-01-22", 150, "Health", "Gym membership", "#fitness"),
]

print("\n[*] Adding Expenses:")
for date, amount, category, notes, tags in expenses_data:
    exp_id = service.add_expense(date, amount, category, notes, tags)
    print(f"  OK {category}: ${amount} on {date} (ID: {exp_id})")

# Set budgets
print("\n\n2. SETTING CATEGORY BUDGETS")
print("-" * 60)

budgets = {
    "Food": 300,
    "Transport": 150,
    "Shopping": 500,
    "Entertainment": 100,
    "Utilities": 600,
    "Health": 200
}

print("\n[$] Setting Budget Limits:")
for category, limit in budgets.items():
    db.set_budget(category, limit)
    print(f"  OK {category}: ${limit}/month")

# Create recurring expenses
print("\n\n3. CREATING RECURRING EXPENSES")
print("-" * 60)

print("\n[~] Recurring Expenses:")
trans_id, rule = recurring_mgr.create_recurring_expense(
    "2025-01-01", 500, "Utilities", "monthly", "Rent payment", "#monthly"
)
print(f"  OK Recurring Rent: ${500}/month starting Jan 1 (ID: {trans_id})")

# Monthly Summary
print("\n\n4. MONTHLY SUMMARY & ANALYSIS")
print("-" * 60)

summary = service.get_month_summary(2025, 1)
print(f"\n[#] January 2025 Summary:")
print(f"  Total Income:    ${summary['total_income']:.2f}")
print(f"  Total Expenses:  ${summary['total_expense']:.2f}")
print(f"  Balance:         ${summary['balance']:.2f}")
print(f"  Transactions:    {summary['count']}")

# Category Summary
print("\n\n5. CATEGORY BREAKDOWN")
print("-" * 60)

category_summary = service.get_category_summary()
print(f"\n[=] Spending by Category:")
for category, amount in sorted(category_summary.items(), key=lambda x: x[1], reverse=True):
    print(f"  {category:20} ${amount:8.2f}")

# Budget Alerts
print("\n\n6. BUDGET ALERTS & STATUS")
print("-" * 60)

alerts = service.check_budget_alerts()
print(f"\n[!] Budget Status:")
for category, alert in alerts.items():
    status_emoji = "G" if alert['status'] == "ok" else "Y" if alert['status'] == "warning" else "O" if alert['status'] == "danger" else "R"
    print(f"  [{status_emoji}] {category:15} ${alert['spent']:7.2f} / ${alert['limit']:7.2f} ({alert['percent']:5.1f}%)")

# Search & Filter
print("\n\n7. SEARCH & FILTER")
print("-" * 60)

print("\n[?] Searching for expenses in 'Food' category:")
food_expenses = service.search_transactions("", category="Food")
for trans in food_expenses:
    print(f"  {trans.date}: ${trans.amount:.2f} - {trans.notes}")

# Sorting
print("\n\n8. SORTING TRANSACTIONS")
print("-" * 60)

print("\n[^] Top 5 expenses by amount:")
sorted_trans = service.get_sorted_transactions(sort_by="amount", ascending=False)
for i, trans in enumerate(sorted_trans[:5], 1):
    print(f"  {i}. {trans.category:15} ${trans.amount:7.2f} on {trans.date}")

# Prediction
print("\n\n9. PREDICTION & RECOMMENDATIONS")
print("-" * 60)

prediction = service.predict_next_month_expense()
print(f"\n[*] Predicted next month expense: ${prediction:.2f}")

rec = service.get_savings_recommendation()
print(f"\n[=] Savings Analysis:")
print(f"  Total Income:            ${rec['total_income']:.2f}")
print(f"  Total Expense:           ${rec['total_expense']:.2f}")
print(f"  Current Balance:         ${rec['current_balance']:.2f}")
print(f"  Recommended Savings:     ${rec['recommended_savings']:.2f}")
if rec['can_achieve']:
    print(f"  Status:                  OK - Achievable")
else:
    print(f"  Status:                  WARNING - Needs expense reduction")

# Export
print("\n\n10. EXPORT FUNCTIONALITY")
print("-" * 60)

print("\n[>] Exporting data...")
csv_success = service.export_to_csv("demo_report.csv")
txt_success = service.export_to_txt("demo_report.txt")

if csv_success:
    print("  OK CSV export: demo_report.csv")
if txt_success:
    print("  OK TXT export: demo_report.txt")

# Final stats
print("\n\n" + "="*60)
print("DEMO SUMMARY")
print("="*60)
print(f"[+] All features demonstrated successfully!")
print(f"   - Created {len(expenses_data)} expenses")
print(f"   - Set {len(budgets)} category budgets")
print(f"   - Generated budget alerts")
print(f"   - Performed search, filter, and sort")
print(f"   - Created predictions and recommendations")
print(f"   - Exported data to CSV and TXT")
print("\n[*] To run the interactive Streamlit app:")
print("   $ streamlit run app.py")
print("\n" + "="*60 + "\n")

db.close()
