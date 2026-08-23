# Smart Expense Tracker & Budget Analyzer

A comprehensive Python course project demonstrating core Python concepts and modern web application development.

## 📋 Features Implemented

### ✅ Core Features (Section I)
1. **Add/Edit/Delete Expenses & Income**
   - Date, amount, category, notes, and tags
   - Separate income and expense tracking
   - Data persistence to SQLite database

2. **Recurring Expenses**
   - Auto-add rent, subscriptions, utilities
   - Monthly/weekly/yearly repetition
   - Smart recurrence engine

3. **Category-wise Budget Limits**
   - Set budget per category (Food, Transport, etc.)
   - Real-time tracking against budget
   - Color-coded alerts at 50%, 80%, 100%

4. **Search & Filter**
   - Search by text (notes, tags, amount)
   - Filter by category, date range, amount range
   - Sort by date, amount, or category

5. **Expense Sorting**
   - Sort ascending/descending
   - Find top expenses quickly
   - Lambda functions for custom sorting

### ✅ Advanced Features (Section II)
6. **Smart Budget Alert System**
   - 🟢 Green (0-50%): OK
   - 🟡 Yellow (50-80%): Warning
   - 🟠 Orange (80-100%): Danger
   - 🔴 Red (100%+): Exceeded

7. **Expense Prediction**
   - Predict next month's expense using NumPy mean
   - Based on historical spending patterns
   - Simple but effective algorithm

8. **Savings Recommendation Engine**
   - Suggest how much to save (20% of income)
   - Calculate achievability
   - Real-life financial guidance

9. **Monthly Comparison Report**
   - Compare two months side-by-side
   - Matplotlib bar charts
   - Track spending trends

10. **Export Reports**
    - CSV export for spreadsheet use
    - TXT export for documents
    - Formatted, ready-to-share reports

11. **Data Validation & Error Handling**
    - Input validation for all fields
    - Try-except error handling
    - User-friendly error messages

12. **Daily/Weekly/Monthly Summaries**
    - Auto-summary at period end
    - Category-wise breakdown
    - Income vs expense comparison

13. **Tags & Notes**
    - Add tags like #college, #travel
    - Search by tags
    - Better transaction classification

## 🛠 Tech Stack

- **Backend**: Python 3.11
- **Database**: SQLite3
- **UI**: Streamlit (modern, responsive web app)
- **Analytics**: NumPy, Pandas, Matplotlib
- **Testing**: unittest

## 📚 Python Topics Covered

### Section I: Fundamentals
- ✅ Variables, data types, operators
- ✅ Control flow (if/elif/else, loops)
- ✅ Functions and recursion
- ✅ String manipulation and methods
- ✅ Comments and indentation
- ✅ Input/Output statements

### Section II: Advanced
- ✅ Lists, Tuples, Sets, Dictionaries
- ✅ List comprehensions
- ✅ Lambda functions (sorting)
- ✅ File handling (CSV, TXT export)
- ✅ Mutable vs Immutable objects
- ✅ Type conversion
- ✅ NumPy arrays (prediction)
- ✅ Matplotlib visualization

## 🚀 Quick Start

### 1. Setup Environment
```powershell
# Create virtual environment
python -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the App
```powershell
# Interactive web app
streamlit run app.py

# This opens at http://localhost:8501
```

### 3. Run Demo
```powershell
# See all features in action
python demo.py
```

### 4. Run Tests
```powershell
# Unit tests for database and services
python tests/test_expense_tracker.py -v

# Output: OK (all 10 tests pass)
```

## 📂 Project Structure

```
expense_tracker/
├── src/expense_tracker/
│   ├── __init__.py           # Package init
│   ├── models.py             # Data models (Transaction, RecurringRule)
│   ├── db.py                 # SQLite database layer
│   ├── services.py           # Business logic (ExpenseService)
│   └── recurring.py          # Recurring expense manager
├── tests/
│   ├── __init__.py
│   └── test_expense_tracker.py  # 10 unit tests
├── app.py                    # Streamlit web app
├── demo.py                   # Demo script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 📊 How to Use (Streamlit App)

### Overview Tab
- See total income, expenses, balance at a glance
- View recent transactions
- Check budget alerts
- See expense breakdown by category (pie & bar charts)

### Add Transaction Tab
- Add expenses (Food, Transport, Shopping, etc.)
- Add income (Salary, Freelance, etc.)
- Include notes and tags for better tracking

### Search & Filter Tab
- Search by keyword, category, amount range
- Sort by date or amount
- Delete old transactions

### Reports Tab
- Monthly summary with category breakdown
- Compare two months side-by-side
- View savings analysis
- Predict next month's spending
- Export as CSV or TXT

### Budget Settings Tab
- Set budget limits per category
- View current budget status
- Adjust limits anytime

## 💡 Key Implementation Details

### Data Model
```python
@dataclass
class Transaction:
    id: Optional[int]
    date: str              # ISO format: 2025-01-15
    amount: float
    category: str
    type: str              # 'expense' or 'income'
    notes: Optional[str]
    tags: Optional[str]    # e.g., "#college,#travel"
```

### Core Services
1. **ExpenseDB** - SQLite CRUD operations
2. **ExpenseService** - Business logic (summaries, alerts, predictions)
3. **RecurringExpenseManager** - Handle monthly recurrence

### Alert System
- Calculates spent % for each category
- Returns status: "ok", "warning", "danger", "exceeded"
- Used in UI for color-coded alerts

### Prediction Algorithm
```python
# Simple average-based prediction
avg_expense = np.mean([all historical expenses])
predicted = avg_expense
```

## 🎓 Course Learning Outcomes

This project covers:

✅ **Control Flow**: if/elif/else, loops, conditional logic  
✅ **Data Structures**: Lists, dicts, sets, tuples  
✅ **Functions**: Definition, arguments, returns, lambdas  
✅ **String Methods**: Split, format, replace, join  
✅ **File Handling**: Read, write, CSV/TXT formats  
✅ **NumPy**: Arrays, mean, average calculations  
✅ **Matplotlib**: Charts, subplots, visualization  
✅ **Error Handling**: Try-except blocks, validation  
✅ **Object-Oriented**: Classes, methods, dataclasses  
✅ **Database**: SQLite CRUD operations  

## 🧪 Testing

Run all tests:
```powershell
python tests/test_expense_tracker.py -v
```

Tests cover:
- ✅ Database CRUD (add, read, delete transactions)
- ✅ Budget management
- ✅ Monthly summaries
- ✅ Category summaries
- ✅ Budget alerts
- ✅ Predictions
- ✅ Service methods

All 10 tests pass ✅

## 📈 Sample Output

```
DEMO SUMMARY
✅ All features demonstrated successfully!
   - Created 8 expenses
   - Set 6 category budgets
   - Generated budget alerts
   - Performed search, filter, and sort
   - Created predictions and recommendations
   - Exported data to CSV and TXT
```

## 🔧 Customization

### Add New Categories
Edit in `app.py`:
```python
expense_category = st.selectbox("Category", 
    ["Food", "Transport", "Shopping", ...])  # Add here
```

### Change Prediction Formula
Edit `services.py` `predict_next_month_expense()`:
```python
def predict_next_month_expense(self):
    expenses = [t.amount for t in trans if t.type == "expense"]
    return np.mean(expenses)  # Change this
```

### Modify Alert Thresholds
Edit `services.py` `check_budget_alerts()`:
```python
if percent >= 100:        # Change 100
    status = "exceeded"
elif percent >= 80:       # Change 80
    status = "danger"
```

## 📱 Future Enhancements

Possible additions:
- 🔐 Password-protected login
- 👥 Multi-user support
- 📲 Mobile app (Flutter/React Native)
- 🤖 ML-based categorization
- 📧 Monthly email reports
- 💳 Bank integration
- 📊 Advanced analytics dashboard

## ⚡ Performance Notes

- SQLite DB: Fast for < 10,000 transactions
- UI: Real-time updates, responsive
- Charts: Generated on-demand
- Exports: < 1 second for typical data

## 📝 License

Course project - Educational use only

## 🤝 Support

For issues:
1. Check the README
2. Run the demo: `python demo.py`
3. Check unit tests: `python tests/test_expense_tracker.py`
4. Review the code comments

## 👨‍🎓 Author

Created as a Python course project demonstrating:
- Core Python fundamentals
- Data structures and algorithms
- File handling and databases
- Scientific computing (NumPy, Matplotlib)
- Web application development (Streamlit)

Enjoy tracking your expenses! 💰📊
