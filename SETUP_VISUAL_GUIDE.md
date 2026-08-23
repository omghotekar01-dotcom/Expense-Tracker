# Google Sheets Setup - Step by Step Visual Guide

## The Easy Way (Recommended)

### Step 1: Download Your Google Credentials

1. Open [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (name it "Expense Tracker")
3. Go to **APIs & Services** → **Credentials**
4. Click **Create Credentials** → **Service Account**

```
┌─────────────────────────────────┐
│ Google Cloud Console            │
├─────────────────────────────────┤
│ APIs & Services → Credentials   │
│                                 │
│ [Create Credentials] ▼          │
│ → Service Account               │
│ → Fill: "expense-tracker"       │
│ → [Create]                      │
└─────────────────────────────────┘
```

5. Find your service account in the list
6. Click on it → **Keys** tab
7. **Add Key** → **Create new key** → **JSON**
8. ⬇️ JSON file downloads to your Downloads folder

### Step 2: Setup Credentials (ONE LINE!)

Open terminal in the expense_tracker folder:

```bash
python setup_credentials.py
```

The script will:
- 🔍 Find your JSON file automatically
- 📋 Verify it's valid
- 📂 Copy to the right location (~/.google_sheets_credentials.json)
- ✅ Show your service account email

**That's it!** Credentials are now set up.

### Step 3: Create & Share Google Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Click **+ Create** → **Spreadsheet**
3. Rename it to **"Expense Tracker"**
4. Click **Share** button (top right)
5. Copy-paste this email (from Step 2 output):
   ```
   xxxxx-xxxxx@xxxxx-gcp.iam.gserviceaccount.com
   ```
6. Set permission to **Editor**
7. Click **Share**

Done! ✅

### Step 4: Run the App

```bash
python -m streamlit run app.py
```

Visit: **http://localhost:8501**

You should see the app fully loaded with no errors!

---

## What's Happening Behind the Scenes

```
Your Computer                Google Cloud               Google Sheets
├─ app.py                    ├─ Service Account         ├─ Transactions
├─ credentials file ────────→│   (has access key)  ────→│ Budgets
└─ (local copy only)         └─                         │ Recurring Rules
                                                        └─
```

**Security**: 
- Your credentials are stored ONLY on your computer
- Not in the code (safe to upload to GitHub)
- Google handles the rest securely

---

## Common Issues & Fixes

### "File not found"
```
Error: No Google service account JSON file found
```

**Fix**: 
1. Download JSON from Google Cloud Console (Step 1)
2. Place in expense_tracker folder
3. Run `python setup_credentials.py` again

### "Invalid JSON"
```
Error: Not a valid service account key
```

**Fix**:
1. Download a fresh JSON from Google Cloud (try again)
2. Make sure you selected "Service Account" type
3. Don't rename or modify the file

### "Credentials not found when running app"
```
Google Sheets Not Connected
```

**Fix**:
1. Verify file exists: `ls ~/.google_sheets_credentials.json`
   - Windows: `dir %USERPROFILE%\.google_sheets_credentials.json`
2. If not there, run: `python setup_credentials.py`
3. Restart the app

### "Permission denied"
```
Error: The caller does not have permission
```

**Fix**:
1. Check you shared the Google Sheet (Step 3)
2. Copy email correctly (no spaces, exact match)
3. Click "Share" button, not just type in box
4. Refresh app and try again

### "Sheet not found"
```
Error: SpreadsheetNotFound
```

**Fix**:
- App will create it automatically
- OR create a sheet named "Expense Tracker" and share it

---

## Verify It's Working

After setup, test with:

```bash
python -c "from src.expense_tracker.db import ExpenseDB; db = ExpenseDB('Test'); print('✅ Connected!' if db.sheets else '❌ Not connected')"
```

Should print: `✅ Connected!`

---

## Quick Reference

| Task | Command |
|------|---------|
| Setup credentials | `python setup_credentials.py` |
| Run app | `python -m streamlit run app.py` |
| Test connection | `python -c "from src.expense_tracker.db import ExpenseDB; db = ExpenseDB('Test'); print('✅ Connected!' if db.sheets else '❌ Failed')"` |
| View Google Sheet | Go to https://sheets.google.com (find "Expense Tracker") |
| Reset credentials | Delete ~/.google_sheets_credentials.json then run setup again |

---

## Key Points

✅ **Three simple steps:**
1. Download JSON from Google Cloud
2. Run `python setup_credentials.py`
3. Share Google Sheet with service account email

✅ **Nothing complicated:**
- Script handles all the technical bits
- Just point to your JSON file
- Done!

✅ **Your data is safe:**
- Stored in your Google Drive
- Automatically backed up
- Can view/edit directly in Google Sheets

✅ **App requirements met:**
- Access from anywhere ✓
- Real-time sync ✓
- Cloud storage ✓
- No local database ✓

---

**You're ready to go!** Follow the 4 steps above and you'll have a cloud-powered expense tracker running in minutes. 🎉
