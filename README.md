# Expense Tracker

A small Python application for recording income and expenses, setting category budgets, and reviewing spending over time. It has a Streamlit interface, a SQLite database, and a command-line demo.

This started as a coursework project, so the code is organised to make the data model, database operations, and reporting logic easy to follow.

## Getting started

Create a virtual environment and install the dependencies:

```powershell
git clone https://github.com/omghotekar01-dotcom/Expense-Tracker.git
cd Expense-Tracker
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Start the browser interface:

```powershell
streamlit run app.py
```

Streamlit prints the local URL, normally `http://localhost:8501`.

If you only want to inspect the logic without using the web interface, run the sample data workflow:

```powershell
python demo.py
```

## Using the app

The sidebar contains views for an overview, adding transactions, searching records, reports, recurring expenses, and budgets.

You can record income or expenses with dates, categories, notes, and tags; review spending totals and category breakdowns; and export reports. Budget alerts compare spending with a configured category limit. The basic prediction is derived from historical expense figures, not from a trained forecasting model.

Transactions and budget limits are stored in a local SQLite database, `expense_tracker.db`, in the working directory by default. The recurring-expense workflow also uses `recurring_rules.json`. Back up these files before resetting your local data.

## Project layout

| Path | Role |
| --- | --- |
| `app.py` | Streamlit interface |
| `src/expense_tracker/models.py` | Transaction data types |
| `src/expense_tracker/db.py` | SQLite tables and queries |
| `src/expense_tracker/services.py` | Calculations, budgets, and report data |
| `src/expense_tracker/recurring.py` | Recurring transaction rules |
| `demo.py` | Sample command-line workflow |
| `tests/test_expense_tracker.py` | Database and service unit tests |

## Running tests

```powershell
python tests/test_expense_tracker.py -v
```

The tests create temporary databases rather than using your everyday expense records.

## Google Sheets notes

This repository also contains setup and implementation notes for Google Sheets. Those are separate from the default SQLite workflow described above. Start with [README_GOOGLE_SHEETS.md](README_GOOGLE_SHEETS.md) and [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md) if you are exploring that integration.

## Limitations

This is a local learning project, not a banking or tax product. Amounts are handled as application numbers and should not be treated as an audited ledger. Prediction and budget outputs are informational and depend on the records you enter.
