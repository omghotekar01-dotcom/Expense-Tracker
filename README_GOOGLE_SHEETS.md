# Smart Expense Tracker & Budget Analyzer - Google Sheets Edition ☁️

## What Is This?

A **production-ready Python application** for tracking expenses, managing budgets, and analyzing spending patterns - now with **cloud storage using Google Sheets**!

All data syncs automatically to Google Sheets in real-time. Access your data from any device, share with family, and enjoy automatic backups.

---

## Quick Start (3 Steps)

### Step 1: Get Your Credentials
```bash
# Download from Google Cloud Console, then:
python setup_credentials.py
```

### Step 2: Share Google Sheet
- Create "Expense Tracker" spreadsheet at sheets.google.com
- Share with the email shown in Step 1
- Give "Editor" permissions

### Step 3: Run the App
```bash
python -m streamlit run app.py
```

Open: **http://localhost:8501**

That's it! Your app is now tracking expenses in Google Sheets. ✅

---

## Documentation

### Getting Started (Pick One)

| Guide | Best For | Time |
|-------|----------|------|
| **START_HERE_GOOGLE_SHEETS.md** | Everyone - read this first! | 5 min |
| **SETUP_VISUAL_GUIDE.md** | Visual learners | 5 min |
| **GOOGLE_SHEETS_SETUP.md** | Detailed step-by-step | 10 min |

### Understanding the Migration

| Document | Purpose |
|----------|---------|
| **GOOGLE_SHEETS_MIGRATION.md** | What changed, why, and benefits |
| **GOOGLE_SHEETS_IMPLEMENTATION.md** | Technical details and architecture |
| **CHANGELOG_GOOGLE_SHEETS.md** | Complete file-by-file breakdown |

### Reference

| Document | Purpose |
|----------|---------|
| **QUICK_START_GOOGLE_SHEETS.md** | Quick reference guide |
| **README.md** | Project overview (original) |
| **USAGE_GUIDE.md** | How to use all features |

---

## All 16 Features ✅

### Core Expense Tracking (7)
- ✅ Add income & expenses
- ✅ Edit & delete transactions  
- ✅ Category management
- ✅ Transaction history
- ✅ Budget limits per category
- ✅ Real-time budget alerts
- ✅ Multi-tag support

### Analytics (4)
- ✅ Monthly summaries
- ✅ Category breakdowns
- ✅ Expense predictions
- ✅ Savings recommendations

### Advanced Features (5)
- ✅ Search & filter
- ✅ Sorting options
- ✅ Recurring expenses
- ✅ Data export (CSV, TXT)
- ✅ Interactive charts

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.11+ |
| **Web Framework** | Streamlit |
| **Storage** | Google Sheets (Cloud) ☁️ |
| **Analytics** | NumPy, Pandas, Matplotlib |
| **Authentication** | Google OAuth (gspread) |

---

## Project Structure

```
expense_tracker/
├── src/expense_tracker/
│   ├── __init__.py
│   ├── models.py          # Data models
│   ├── db.py              # Google Sheets integration
│   ├── services.py        # Business logic (25+ functions)
│   └── recurring.py       # Recurring expenses
├── tests/
│   └── test_expense_tracker.py  # 10 unit tests
├── app.py                 # Streamlit web UI (5 pages)
├── demo.py                # Feature demonstration
├── requirements.txt       # Dependencies
├── setup_credentials.py   # Credential setup tool
└── [DOCUMENTATION FILES]  # Guides and references
```

---

## How It Works

### Data Flow
```
User Input → Streamlit UI → ExpenseService → ExpenseDB → Google Sheets
                                                              ↓
                                                         Real-time sync
                                                              ↓
                                                    Visible in browser
```

### Storage
- **Transactions Sheet**: id, date, amount, category, type, notes, tags
- **Budgets Sheet**: id, category, budget_limit
- **Recurring Rules Sheet**: id, transaction_id, interval, next_date

**No local database needed** - everything is in Google Sheets! ☁️

---

## Key Features

### 🌐 Cloud-Based
- Access from **any device**
- No local file to manage
- Mobile-friendly via Google Sheets app

### ⚡ Real-Time Sync
- Changes appear instantly
- No manual save needed
- Automatic backup

### 🔐 Secure
- Google's enterprise encryption
- Credentials protected
- Audit trail of changes

### 👥 Shareable
- Share with family members
- Team access supported
- View/edit in Google Sheets directly

### 📊 Professional
- 5-page Streamlit interface
- Interactive charts
- Real-time budget alerts
- Complete analytics

---

## Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

Required packages:
- streamlit - Web UI framework
- pandas, numpy - Data analysis
- matplotlib - Charts
- gspread - Google Sheets API
- google-auth-* - Google authentication

### 2. Setup Google Credentials
```bash
python setup_credentials.py
```

This will:
- Find your Google service account JSON
- Validate it
- Copy to secure location
- Display service account email

### 3. Create & Share Google Sheet
1. Go to https://sheets.google.com
2. Create new spreadsheet
3. Name it: "Expense Tracker"
4. Share with email from step 2
5. Give "Editor" permissions

### 4. Run the App
```bash
python -m streamlit run app.py
```

Visit: **http://localhost:8501**

---

## Usage Examples

### Add an Expense
```python
# Via Web UI (easiest)
# Open http://localhost:8501 → Add Transaction page
# Fill in: Date, Amount, Category, Type, Notes
# Click "Add Expense" → Done! 💰

# Via Code (if needed)
from src.expense_tracker.services import ExpenseService
from src.expense_tracker.db import ExpenseDB

db = ExpenseDB("Expense Tracker")
service = ExpenseService(db)
service.add_expense("2025-01-15", 50.00, "Food", "Grocery shopping")
```

### Check Budget Status
```python
# View alerts for all categories
alerts = service.check_budget_alerts()
for category, alert in alerts.items():
    print(f"{category}: {alert['status']}")
    # Output: "Food: ok", "Transport: warning", etc.
```

### Get Monthly Summary
```python
summary = service.get_month_summary()
print(f"Income: ${summary['total_income']}")
print(f"Expenses: ${summary['total_expense']}")
print(f"Balance: ${summary['balance']}")
```

### Export Data
```python
service.export_to_csv("monthly_report.csv")
service.export_to_txt("monthly_report.txt")
```

---

## Security

### Credentials Protection ✅
- File: `~/.google_sheets_credentials.json` (permissions: 600)
- Environment: `GOOGLE_SHEETS_CREDENTIALS` env variable
- Both methods supported (local development & cloud deployment)

### Data Protection ✅
- HTTPS encryption (Google Sheets)
- AES-256 encryption at rest
- OAuth 2.0 authentication
- Access logs available

### Best Practices ✅
- `.gitignore` excludes credential files
- Never commit secrets to repository
- Use environment variables for production
- Audit trail available in Google Drive

---

## Testing

### Run Unit Tests
```bash
# All tests (10/10 passing)
python -m pytest tests/test_expense_tracker.py -v

# Specific test
python -m pytest tests/test_expense_tracker.py::test_add_expense -v
```

### Run Demo
```bash
# Shows all features working
python demo.py
```

### Manual Testing
1. Open http://localhost:8501
2. Create an expense
3. Check Google Sheet - data appears instantly!
4. Edit the expense in Google Sheets
5. Refresh app - changes visible

---

## Performance

### Speed
- **Write**: <1 second (typical)
- **Read**: <1 second for <1000 rows
- **UI**: Instant with Streamlit caching

### Limits
- **API Rate**: 100 requests/minute (typical: <10/min)
- **Sheet Size**: 10M cells (supports millions of transactions)
- **Users**: Unlimited concurrent

### Optimization
- Streamlit auto-caches repeated reads
- Batch operations for bulk import
- Archive old data to separate sheets for large datasets

---

## Troubleshooting

### "Google Sheets Not Connected"
```bash
# Solution: Setup credentials
python setup_credentials.py

# Verify:
ls ~/.google_sheets_credentials.json
```

### "Permission Denied"
```
1. Go to Google Sheet
2. Click Share
3. Add service account email (from step 2)
4. Give "Editor" permissions
5. Refresh app
```

### "SpreadsheetNotFound"
```
App creates it automatically if missing
Or create manually and name it "Expense Tracker"
```

### Slow Performance
```
1. Archive old data to separate sheet
2. Use filtering/date ranges
3. Clear browser cache (Ctrl+Shift+Del)
```

---

## Deployment

### Local Development
```bash
python setup_credentials.py  # One-time setup
python -m streamlit run app.py
```

### Streamlit Cloud
```bash
# Add to Streamlit secrets (Settings → Secrets)
GOOGLE_SHEETS_CREDENTIALS="<paste JSON string here>"

# Push code to GitHub (credentials not in code)
# No other changes needed!
```

### Docker
```dockerfile
ENV GOOGLE_SHEETS_CREDENTIALS="<json>"
RUN pip install -r requirements.txt
CMD streamlit run app.py
```

---

## API Reference

### ExpenseDB (Google Sheets Backend)
```python
db = ExpenseDB("Sheet Name")

# CRUD Operations
db.add_transaction(trans) → int
db.get_transactions(start_date, end_date) → List[Transaction]
db.delete_transaction(id) → bool

# Budget Management
db.set_budget(category, limit) → bool
db.get_budgets() → dict

# Recurring Expenses
db.add_recurring_rule(rule) → int
db.get_recurring_rules() → List[RecurringRule]
db.update_recurring_rule(id, next_date) → bool
```

### ExpenseService (Business Logic)
```python
service = ExpenseService(db)

# Transactions
service.add_expense(date, amount, category, notes, tags) → int
service.add_income(date, amount, source, notes) → int
service.delete_expense(id) → bool

# Analytics
service.get_month_summary() → dict
service.get_category_summary() → dict
service.check_budget_alerts() → dict
service.predict_next_month_expense() → float
service.get_savings_recommendation() → dict

# Search & Export
service.search_transactions(category, type, tags) → List[Transaction]
service.get_sorted_transactions(by) → List[Transaction]
service.export_to_csv(filename) → bool
service.export_to_txt(filename) → bool
```

---

## Development

### Contributing
1. Fork repository
2. Create feature branch
3. Make changes
4. Add tests if applicable
5. Submit pull request

### Adding Features
1. Update `services.py` for business logic
2. Update `db.py` for data persistence
3. Update `app.py` for UI
4. Add tests to `tests/`
5. Update documentation

---

## FAQ

**Q: Can I access data offline?**  
A: No, but Google Sheets can be downloaded for offline access.

**Q: Can multiple people use the same sheet?**  
A: Yes! Share the Google Sheet - changes sync automatically.

**Q: Is my data backed up?**  
A: Yes - Google Drive automatically backs up all versions.

**Q: Can I export to other formats?**  
A: Yes - app supports CSV and TXT. Google Sheets supports Excel export.

**Q: What if I lose internet?**  
A: App won't work, but data is safe in Google Sheets.

**Q: Can I use different Google account?**  
A: Yes - just change credentials in `setup_credentials.py`

---

## Resources

- [Streamlit Docs](https://docs.streamlit.io/)
- [gspread Documentation](https://docs.gspread.org/)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [Python Documentation](https://docs.python.org/)

---

## License

This project is provided as-is for educational purposes.

---

## Credits

**Created**: December 2025  
**Version**: 2.0 (Google Sheets Edition)  
**Status**: Production Ready ✅

---

## Quick Links

- 📖 **START_HERE_GOOGLE_SHEETS.md** - Read this first!
- 🚀 **SETUP_VISUAL_GUIDE.md** - Visual setup guide
- 🔧 **GOOGLE_SHEETS_SETUP.md** - Detailed setup
- 📋 **USAGE_GUIDE.md** - How to use features

---

**Your cloud-powered expense tracker is ready!** ☁️

Open: **http://localhost:8501**

Start tracking expenses now! 💰📊
