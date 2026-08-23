# Smart Expense Tracker & Budget Analyzer

A comprehensive Python course project demonstrating core Python concepts, data structures, file handling, NumPy/Matplotlib, and modern web development.

## 🎯 Quick Start

```powershell
# 1. Setup
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Run Demo (shows all features)
python demo.py

# 3. Run Tests (10 tests, all passing)
python tests/test_expense_tracker.py -v

# 4. Launch Web App
streamlit run app.py
```

**App runs at:** `http://localhost:8501`

## ✨ Features (16 Total)

### Core Features
✅ Add/edit/delete expenses & income  
✅ Recurring expenses (auto-add)  
✅ Category budget limits with alerts  
✅ Search/filter/sort transactions  
✅ Notes & tags for classification  

### Analytics & Reports
✅ Monthly summaries with charts  
✅ Budget alert system (50/80/100%)  
✅ Expense prediction (NumPy)  
✅ Savings recommendations  
✅ Monthly comparison reports  
✅ Export to CSV/TXT  

### Advanced
✅ Data validation & error handling  
✅ Professional unit tests (10 tests)  
✅ Modern Streamlit UI  
✅ SQLite database  
✅ Data visualization (Matplotlib)  

## 📚 Python Topics Covered

**Section I:** Variables, operators, control flow, loops, strings, functions  
**Section II:** Lists, dicts, sets, tuples, file handling, NumPy, Matplotlib

[Full list in SUBMISSION_GUIDE.md →](SUBMISSION_GUIDE.md)

## 📂 Project Structure

```
src/expense_tracker/
  ├── models.py         # Data models
  ├── db.py             # SQLite layer
  ├── services.py       # Business logic
  └── recurring.py      # Recurring expenses

tests/
  └── test_expense_tracker.py  # 10 unit tests ✅

app.py                  # Streamlit web UI
demo.py                 # Demo script
requirements.txt        # Dependencies
```

## 🎮 How to Use

### Option 1: Interactive Web App
```powershell
streamlit run app.py
```
- 📊 Overview (income, expenses, charts)
- ➕ Add transactions
- 🔍 Search & filter
- 📈 Reports & analytics
- ⚙️ Budget settings

### Option 2: Demo Script
```powershell
python demo.py
```
Shows all features with sample data (2-3 minutes)

### Option 3: Python API
```python
from src.expense_tracker import ExpenseService, ExpenseDB

db = ExpenseDB("my_data.db")
service = ExpenseService(db)

# Add expense
service.add_expense("2025-01-15", 50, "Food", "Lunch")

# Get monthly summary
summary = service.get_month_summary(2025, 1)

# Check budget alerts
alerts = service.check_budget_alerts()
```

## 🧪 Testing

```powershell
python tests/test_expense_tracker.py -v
```

**Output:**
```
Ran 10 tests in 0.2s
OK ✅
```

Tests cover:
- Database CRUD operations
- Monthly/category summaries
- Budget alerts
- Predictions
- Service methods

## 📊 Sample Features

### Budget Alerts
- 🟢 0-50%: OK
- 🟡 50-80%: Warning
- 🟠 80-100%: Danger
- 🔴 100%+: Exceeded

### Predictions
Uses NumPy mean() to predict next month's expenses based on history

### Export
- CSV for Excel/spreadsheets
- TXT for documents/reports

## 🔧 Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.11+ |
| Database | SQLite |
| UI | Streamlit |
| Analytics | NumPy, Pandas |
| Visualization | Matplotlib |
| Testing | unittest |

## 📖 Documentation

- **README.md** - This file
- **USAGE_GUIDE.md** - Detailed usage instructions
- **SUBMISSION_GUIDE.md** - Course project submission info
- Code comments throughout

## 🎓 What You'll Learn

✅ Python fundamentals (variables, operators, control flow)  
✅ Data structures (lists, dicts, sets, tuples)  
✅ Functions & lambdas  
✅ File I/O & databases  
✅ NumPy for predictions  
✅ Matplotlib for charts  
✅ Error handling (try-except)  
✅ Unit testing  
✅ Web development (Streamlit)  
✅ Software design patterns  

## 🚀 Next Steps

1. **Run the demo:** `python demo.py`
2. **Explore the code:** Check `src/expense_tracker/`
3. **Launch the app:** `streamlit run app.py`
4. **Run tests:** `python tests/test_expense_tracker.py`
5. **Customize:** Edit categories, budgets, thresholds

## 💡 Key Files to Review

For examiners/learners:
1. `src/expense_tracker/db.py` - Database layer with SQLite
2. `src/expense_tracker/services.py` - Business logic with NumPy
3. `src/expense_tracker/models.py` - Data design patterns
4. `app.py` - Modern Streamlit UI
5. `tests/test_expense_tracker.py` - Professional testing

## ⚡ Performance

- SQLite DB: Handles thousands of transactions
- UI: Real-time updates, responsive
- Charts: Generated on-demand
- Exports: < 1 second

## 📝 Requirements.txt

```
streamlit>=1.20.0
pandas>=1.5.0
numpy>=1.23.0
matplotlib>=3.6.0
python-dateutil>=2.8.2
```

## 🤝 Support

Questions? Check:
1. README.md & USAGE_GUIDE.md
2. Run `python demo.py` to see everything in action
3. Review code comments in `src/expense_tracker/`
4. Check unit tests for usage examples

## 📄 License

Educational project - Course submission

---

**Ready to track your expenses smartly!** 💰📊

For detailed guide: [USAGE_GUIDE.md](USAGE_GUIDE.md)  
For course submission info: [SUBMISSION_GUIDE.md](SUBMISSION_GUIDE.md)
