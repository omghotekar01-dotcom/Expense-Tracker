# Google Sheets Setup Guide

The Expense Tracker now uses Google Sheets for cloud-based data storage instead of SQLite.

## Setup Instructions

### 1. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project: Click "Select a Project" → "New Project" → Enter name → Create
3. Wait for project creation to complete

### 2. Enable Google Sheets API

1. In Google Cloud Console, go to APIs & Services
2. Click "Enable APIs and Services"
3. Search for "Google Sheets API"
4. Click it and press "Enable"
5. Repeat for "Google Drive API" (needed for file access)

### 3. Create Service Account

1. Go to APIs & Services → Credentials
2. Click "Create Credentials" → Service Account
3. Fill in:
   - Service account name: `expense-tracker`
   - Service account ID: (auto-filled)
   - Click "Create and Continue"
4. Skip optional steps, click "Done"

### 4. Create and Download Key

1. In Credentials, under "Service Accounts", click the service account you just created
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Choose "JSON" → "Create"
5. A JSON file will download automatically - **save this carefully**

### 5. Setup Credentials (Choose One Method)

**Method A: Local File (for development)**

1. Copy the downloaded JSON file to your home directory:
   ```
   ~/.google_sheets_credentials.json
   ```
   - Windows: `C:\Users\YourUsername\.google_sheets_credentials.json`
   - Mac/Linux: `~/.google_sheets_credentials.json`

**Method B: Environment Variable (for production/Streamlit Cloud)**

1. Set the environment variable with the entire JSON content:
   ```
   GOOGLE_SHEETS_CREDENTIALS=<paste_entire_json_here>
   ```

### 6. Share Google Sheet with Service Account

1. Find the email in your downloaded JSON file (looks like `...@...-gcp.iam.gserviceaccount.com`)
2. Create a new Google Sheet at [sheets.google.com](https://sheets.google.com)
3. Click "Share" and add the service account email with Editor permissions
4. Or let the app create it automatically (it will on first run)

## Testing Connection

Run the app:
```bash
python -m streamlit run app.py --server.headless=true
```

You should see: `Connected to Google Sheet: Expense Tracker`

## Troubleshooting

**"Credentials not found"**
- Verify JSON file is in `~/.google_sheets_credentials.json`
- Or set `GOOGLE_SHEETS_CREDENTIALS` environment variable

**"Permission denied"**
- Ensure service account email is shared on the Google Sheet
- Check service account has Editor permissions

**"SpreadsheetNotFound"**
- The app will create the sheet automatically if missing
- Make sure you've completed "Share Google Sheet" step if creating manually

## Features

- ✅ All data synced to Google Sheets in real-time
- ✅ Access data from multiple devices/locations
- ✅ Built-in backup and version history (Google Drive)
- ✅ Shareable with team members (give them access to the Sheet)
- ✅ No local database file needed

## Security Note

- Keep your `service-account-key.json` file **secret** - don't commit to GitHub
- The `.gitignore` already excludes `*credentials*.json` files
- For production, use environment variables instead of files
