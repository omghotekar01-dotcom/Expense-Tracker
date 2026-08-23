# Google Sheets Migration Guide

## What Changed?

The Expense Tracker has been migrated from **SQLite** (local file storage) to **Google Sheets** (cloud storage).

### Benefits

✅ **Cloud Storage** - Access data anywhere, any device  
✅ **Real-time Sync** - Changes visible instantly across all devices  
✅ **Built-in Backup** - Google Drive automatically backs up all versions  
✅ **Team Sharing** - Share the sheet with family/team members  
✅ **No Local Database** - No `instance.db` file cluttering your computer  
✅ **Mobile Friendly** - View/edit data on mobile via Google Sheets app  

## Quick Start

### 1. Install Updated Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Google Sheets Credentials

**Option A: Automatic Setup (Recommended)**
```bash
python setup_credentials.py
```

**Option B: Manual Setup**
- Follow detailed instructions in `GOOGLE_SHEETS_SETUP.md`

### 3. Run the App
```bash
python -m streamlit run app.py
```

The app will automatically:
- Create a Google Sheet named "Expense Tracker"
- Create three worksheets: transactions, budgets, recurring_rules
- Sync all operations to Google Sheets

## How It Works

### Data Structure

**Transactions Sheet**
- Columns: id, date, amount, category, type, notes, tags
- Each row is a transaction

**Budgets Sheet**
- Columns: id, category, budget_limit
- Category-wise budget limits

**Recurring Rules Sheet**
- Columns: id, transaction_id, interval, next_date
- Recurring expense configuration

### Syncing

All CRUD operations automatically sync to Google Sheets:
- Add expense → Appends row to transactions sheet
- Add budget → Appends/updates budgets sheet
- Delete transaction → Deletes row from sheet
- etc.

No manual save needed - everything is live!

## Troubleshooting

**"Google Sheets Not Connected"**
1. Verify credentials file at: `~/.google_sheets_credentials.json`
2. Run setup script again: `python setup_credentials.py`
3. Check Google Sheets API is enabled in Google Cloud Console

**"Permission denied"**
1. Copy service account email from the credentials JSON
2. Share the Google Sheet with that email (Editor permissions)
3. Try again

**Slow Performance**
- Google Sheets API has rate limits (~100 requests/min)
- Large sheets (1000+ rows) load slower
- For better performance, archive old data to a different sheet

## Credentials Security

⚠️ **Important:** Your credentials file contains sensitive keys

```bash
# Never commit to Git - already in .gitignore
git check-ignore .google_sheets_credentials.json  # should show file is ignored

# File permissions are secure
ls -la ~/.google_sheets_credentials.json  # should show -rw------- (600)
```

## Local Development vs Production

### Local Development
```bash
# Uses file-based credentials
~/.google_sheets_credentials.json
```

### Production (Streamlit Cloud)
```bash
# Uses environment variable
GOOGLE_SHEETS_CREDENTIALS=<json_string_here>
```

Set this in Streamlit Cloud → App Settings → Secrets

## Migration from SQLite

If you have existing SQLite data:

1. **Export from SQLite**:
   ```python
   # Temporarily use old SQLite database
   from src.expense_tracker.db import ExpenseDB
   db = ExpenseDB("old_instance.db")  # your old file
   transactions = db.get_transactions()
   
   # Copy to Google Sheets
   # ... (create script to import)
   ```

2. **Use Google Sheets moving forward** - no further SQLite interaction needed

## API Details

### ExpenseDB Methods (unchanged interface)
```python
db = ExpenseDB("Expense Tracker")

# All operations work the same
db.add_transaction(trans)
db.get_transactions(start_date, end_date)
db.delete_transaction(trans_id)
db.set_budget(category, limit)
db.get_budgets()
```

The implementation changed, but the API is the same - no service layer changes needed!

## Next Steps

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Set up credentials: `python setup_credentials.py`
3. ✅ Run the app: `python -m streamlit run app.py`
4. ✅ Open in browser: `http://localhost:8501`
5. ✅ Start tracking expenses!

## Support

For detailed setup help, see:
- `GOOGLE_SHEETS_SETUP.md` - Step-by-step instructions
- `setup_credentials.py` - Automated setup
- GitHub Issues - Report problems
