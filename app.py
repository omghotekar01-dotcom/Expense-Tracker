"""Main Streamlit application"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import sys
from pathlib import Path
import json
from src.expense_tracker.recurring import RecurringExpenseManager

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from expense_tracker.db import ExpenseDB
from expense_tracker.services import ExpenseService
from expense_tracker.models import Transaction

# Cache database and service to avoid thread issues
@st.cache_resource
def get_db():
    return ExpenseDB()

@st.cache_resource
def get_service():
    db = get_db()
    return ExpenseService(db)


db = get_db()
service = get_service()

recurring_manager = RecurringExpenseManager(db)

# Load recurring rules from JSON file
RECURRING_RULES_PATH = "recurring_rules.json"
def load_recurring_rules():
    try:
        with open(RECURRING_RULES_PATH, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_recurring_rules(rules):
    with open(RECURRING_RULES_PATH, "w") as f:
        json.dump(rules, f, indent=2)

# Process due recurring expenses at app start
rules = load_recurring_rules()
new_ids = recurring_manager.process_recurring_expenses(rules)
if new_ids:
    save_recurring_rules(rules)

# Check database status
if not db.using_sqlite:
    st.error("""
    Database Error

    Failed to initialize SQLite database.
    Please check your setup and restart the app.
    """)
    st.stop()

# Sidebar Navigation
st.sidebar.title("💰 Expense Tracker")
page = st.sidebar.radio(
    "Navigation",
    [
        "📊 Overview",
        "➕ Add Transaction",
        "🔍 Search & Filter",
        "📈 Reports",
        "🔁 Recurring Expenses",
        "⚙️ Budget Settings",
        "👨‍💻 Developer Options"
    ]
)

if page == "📊 Overview":
    st.title("📊 Dashboard Overview")
    # Get current month
    today = datetime.now()
    year, month = today.year, today.month

    # Summary cards
    summary = service.get_month_summary(year, month)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Income", f"${summary['total_income']:.2f}")
    with col2:
        st.metric("Total Expenses", f"${summary['total_expense']:.2f}")
    with col3:
        st.metric("Balance", f"${summary['balance']:.2f}")
    with col4:
        st.metric("Transactions", summary['count'])

    st.divider()

    # Quick Summary
    st.subheader("📋 Quick Summary")
    today_str = today.strftime("%Y-%m-%d")
    transactions_today = [t for t in db.get_transactions() if t.date[:10] == today_str and t.type == "expense"]
    total_today = sum(t.amount for t in transactions_today)
    month_str = today.strftime("%Y-%m")
    transactions_month = [t for t in db.get_transactions() if t.date[:7] == month_str and t.type == "expense"]
    total_month = sum(t.amount for t in transactions_month)
    budgets = db.get_budgets()
    total_budget = sum(budgets.values())
    remaining_budget = total_budget - total_month if total_budget > 0 else None
    col1, col2, col3 = st.columns(3)
    col1.metric("Spent Today", f"${total_today:.2f}")
    col2.metric("Spent This Month", f"${total_month:.2f}")
    if remaining_budget is not None:
        col3.metric("Remaining Budget", f"${remaining_budget:.2f}")
        percent_used = (total_month / total_budget * 100) if total_budget > 0 else 0
        if percent_used >= 100:
            st.error("⚠️ You have exceeded your monthly budget!")
        elif percent_used >= 80:
            st.warning("⚠️ You have used over 80% of your monthly budget.")
    else:
        col3.info("No budget set")

    st.divider()

    # Category Analytics
    st.subheader("📊 Category Analytics")
    cat_summary = service.get_category_summary()
    if cat_summary:
        highest_cat = max(cat_summary, key=cat_summary.get)
        lowest_cat = min(cat_summary, key=cat_summary.get)
        st.info(f"Highest spending category: **{highest_cat}** (${cat_summary[highest_cat]:.2f})")
        st.info(f"Lowest spending category: **{lowest_cat}** (${cat_summary[lowest_cat]:.2f})")
    else:
        st.info("No category analytics available yet.")

    st.divider()

    # Budget Alerts
    st.subheader("⚠️ Budget Alerts")
    alerts = service.check_budget_alerts()
    if alerts:
        for category, alert in alerts.items():
            color = ""
            if alert['status'] == "exceeded":
                color = "🔴"
            elif alert['status'] == "danger":
                color = "🟠"
            elif alert['status'] == "warning":
                color = "🟡"
            else:
                color = "🟢"
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"{color} **{category}**: ${alert['spent']:.2f} / ${alert['limit']:.2f} ({alert['percent']:.1f}%)")
            with col2:
                progress = min(alert['percent'] / 100, 1.0)
                st.progress(progress, text=alert['status'].upper())

    # Expense by Category Chart
    st.subheader("📊 Expense Breakdown")
    category_data = service.get_category_summary()
    if category_data:
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.pie(category_data.values(), labels=category_data.keys(), autopct='%1.1f%%', startangle=90)
            ax.set_title("Expense Distribution by Category")
            st.pyplot(fig)
        with col2:
            fig, ax = plt.subplots(figsize=(8, 5))
            categories = list(category_data.keys())
            amounts = list(category_data.values())
            ax.bar(categories, amounts, color=['#667eea', '#764ba2', '#f093fb', '#4facfe'])
            ax.set_ylabel("Amount ($)")
            ax.set_title("Expense by Category")
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)
    else:
        st.info("No expenses recorded yet.")

    st.divider()
    st.subheader("📝 Recent Transactions")
    trans = db.get_transactions()[:10]
    if trans:
        df_data = []
        for idx, t in enumerate(trans, 1):
            df_data.append({
                "#": idx,
                "Date": t.date,
                "Type": t.type.upper(),
                "Category": t.category,
                "Amount": f"${t.amount:.2f}",
                "Notes": t.notes or "-",
                "Tags": t.tags or "-"
            })
        df = pd.DataFrame(df_data)
        st.dataframe(df, width='stretch')
    else:
        st.info("No transactions yet. Add one in the 'Add Transaction' section!")

# === PAGE: ADD TRANSACTION ===
elif page == "➕ Add Transaction":
    st.title("➕ Add Transaction")
    st.divider()
    st.subheader("Quick Add Recurring Expense")
    with st.form("recurring_form"):
        rec_date = st.date_input("Start Date", datetime.now(), key="rec_date")
        rec_amount = st.number_input("Amount ($)", min_value=0.0, step=0.01, key="rec_amount")
        rec_category = st.text_input("Category", key="rec_category")
        rec_interval = st.selectbox("Interval", ["weekly", "monthly", "yearly"], key="rec_interval")
        rec_notes = st.text_input("Notes (optional)", key="rec_notes")
        rec_tags = st.text_input("Tags (optional)", key="rec_tags")
        submit_rec = st.form_submit_button("Add Recurring Expense", use_container_width=True)
        if submit_rec:
            if rec_amount <= 0:
                st.error("Amount must be positive.")
            elif not rec_category:
                st.error("Category cannot be empty.")
            else:
                rec_date_str = rec_date.isoformat() if rec_date else datetime.now().date().isoformat()
                _, rule = recurring_manager.create_recurring_expense(
                    rec_date_str, rec_amount, rec_category, rec_interval, rec_notes, rec_tags
                )
                rules = load_recurring_rules()
                rules.append(rule)
                save_recurring_rules(rules)
                st.success("✅ Recurring expense added!")
                st.rerun()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Add Expense")
        if 'expense_msg' in st.session_state:
            st.success(st.session_state.expense_msg)
            del st.session_state['expense_msg']
        if 'expense_err' in st.session_state:
            st.error(st.session_state.expense_err)
            del st.session_state['expense_err']
        with st.form("expense_form"):
            expense_date = st.date_input("Date (default: today)", datetime.now())
            expense_amount = st.number_input("Amount ($)", min_value=0.0, step=0.01)
            predefined_categories = ["Food", "Transport", "Shopping", "Entertainment", "Utilities", "Health", "Other"]
            expense_category = st.selectbox("Category (suggested)", predefined_categories)
            custom_category = st.text_input("Or enter custom category")
            final_category = custom_category.strip() if custom_category.strip() else expense_category
            expense_notes = st.text_input("Notes (optional)")
            expense_tags = st.text_input("Tags (e.g., #travel, #college)")
            submit_expense = st.form_submit_button("Add Expense", use_container_width=True)
            if submit_expense:
                if expense_amount <= 0:
                    st.session_state['expense_err'] = "Amount must be positive."
                    st.rerun()
                elif not final_category:
                    st.session_state['expense_err'] = "Category cannot be empty."
                    st.rerun()
                else:
                    expense_date_str = expense_date.isoformat() if expense_date else datetime.now().date().isoformat()
                    trans_id = service.add_expense(
                        expense_date_str,
                        expense_amount,
                        final_category,
                        expense_notes,
                        expense_tags
                    )
                    st.session_state['expense_msg'] = f"✅ Expense added! (ID: {trans_id})"
                    st.rerun()

    with col2:
        st.subheader("Add Income")
        if 'income_msg' in st.session_state:
            st.success(st.session_state.income_msg)
            del st.session_state['income_msg']
        if 'income_err' in st.session_state:
            st.error(st.session_state.income_err)
            del st.session_state['income_err']
        with st.form("income_form"):
            income_date = st.date_input("Date (default: today)", datetime.now(), key="income_date")
            income_amount = st.number_input("Amount ($)", min_value=0.0, step=0.01, key="income_amount2")
            predefined_sources = ["Salary", "Freelance", "Investment", "Gift", "Other"]
            income_source = st.selectbox("Source (suggested)", predefined_sources, key="income_source")
            custom_source = st.text_input("Or enter custom source", key="custom_income_source")
            final_source = custom_source.strip() if custom_source.strip() else income_source
            income_notes = st.text_input("Notes (optional)", key="income_notes2")
            submit_income = st.form_submit_button("Add Income", use_container_width=True)
            if submit_income:
                if income_amount <= 0:
                    st.session_state['income_err'] = "Amount must be positive."
                    st.rerun()
                elif not final_source:
                    st.session_state['income_err'] = "Source cannot be empty."
                    st.rerun()
                else:
                    income_date_str = income_date.isoformat() if income_date else datetime.now().date().isoformat()
                    try:
                        trans_id = service.add_income(
                            income_date_str,
                            income_amount,
                            final_source,
                            income_notes
                        )
                        st.session_state['income_msg'] = f"✅ Income added! (ID: {trans_id})"
                        st.rerun()
                    except Exception as e:
                        st.session_state['income_err'] = f"❌ Failed to add income: {e}"
                        st.rerun()
# === PAGE: DEVELOPER OPTIONS ===
elif page == "👨‍💻 Developer Options":
    st.title("👨‍💻 Developer Options & Project Info")
    st.subheader("Group Members")
    dev_data = [
        ["Nupur Agarwal", "1030439", "1251030483"],
        ["Om Patil", "1030440", "1251030402"],
        ["Om Ghotekar", "1030441", "1251030180"],
        ["Nandkishor Pachmahi", "1030442", "1251030142"]
    ]
    dev_df = pd.DataFrame(dev_data, columns=["Name", "Roll No", "PRN"])
    st.table(dev_df)

    st.subheader("Project Information")
    st.markdown("""
**Project Title:** Smart Expense Tracker  
**Description:**
> A modern, user-friendly expense tracker web application built with Python and Streamlit. It allows users to add, view, search, and analyze expenses and incomes, set budgets, and visualize data with interactive charts. Data is stored locally using SQLite for privacy and speed.

**Key Features:**
- Add, view, and search transactions
- Set and monitor category budgets
- Modern UI with interactive charts (donut, bar)
- Data export (CSV, TXT)
- Responsive and easy to use

**Tools & Technologies Used:**
- Python 3.11
- Streamlit (web UI)
- Pandas (data handling)
- Matplotlib (visualization)
- SQLite (local database)

**Developed for:** Python Course Project
    """)

# === PAGE: SEARCH & FILTER ===
elif page == "🔍 Search & Filter":
    st.title("🔍 Search & Filter Transactions")
    col1, col2, col3 = st.columns(3)
    with col1:
        search_query = st.text_input("Search (notes/tags/amount)")
    with col2:
        filter_category = st.selectbox("Filter by Category", [None, "Food", "Transport", "Shopping", "Entertainment", "Utilities", "Health", "Other", "Salary", "Freelance"])
    with col3:
        sort_by = st.selectbox("Sort by", ["date", "amount", "category"])
    col1, col2 = st.columns(2)
    with col1:
        min_amount = st.number_input("Min Amount ($)", min_value=0.0, step=0.01)
    with col2:
        max_amount = st.number_input("Max Amount ($)", min_value=0.0, step=0.01, value=100000.0)

    results = service.search_transactions(search_query, filter_category, min_amount if min_amount > 0 else None, max_amount)
    results = service.get_sorted_transactions(sort_by)  # Apply sorting

    st.subheader(f"Found {len(results)} transactions")
    if results:
        df_data = []
        for idx, t in enumerate(results, 1):
            df_data.append({
                "#": idx,
                "Date": t.date,
                "Type": t.type.upper(),
                "Category": t.category,
                "Amount": f"${t.amount:.2f}",
                "Notes": t.notes or "-",
                "Tags": t.tags or "-"
            })
        df = pd.DataFrame(df_data)
        st.dataframe(df, width='stretch')
    else:
        st.info("No transactions found.")


elif page == "🔁 Recurring Expenses":
    st.title("🔁 Manage Recurring Expenses")
    rules = load_recurring_rules()
    if rules:
        df_rules = []
        for idx, rule in enumerate(rules, 1):
            df_rules.append({
                "#": idx,
                "Next Date": rule["next_date"][:10],
                "Amount": f"${rule['original_amount']:.2f}",
                "Category": rule["original_category"],
                "Interval": rule["interval"],
                "Notes": rule.get("original_notes", "-"),
                "Tags": rule.get("original_tags", "-")
            })
        st.dataframe(pd.DataFrame(df_rules), width='stretch')
        st.info("Recurring expenses are auto-added on or after their next date.")
        # Option to remove a rule
        remove_idx = st.number_input("Remove recurring rule #", min_value=1, max_value=len(rules), step=1, key="remove_rec")
        if st.button("Remove", key="remove_btn", width='stretch'):
            rules.pop(remove_idx-1)
            save_recurring_rules(rules)
            st.success("Recurring rule removed.")
            st.rerun()
    else:
        st.info("No recurring expenses set yet. Add one from the Add Transaction page.")

# === PAGE: REPORTS ===
elif page == "📈 Reports":
    st.title("📈 Reports & Analytics")

    report_type = st.selectbox("Select Report Type", 
        ["Monthly Summary", "Monthly Comparison", "Savings Analysis", "Prediction", "Export Data", "Import Data"])

    if report_type == "Import Data":
        st.subheader("Import Expenses from CSV")
        uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
        if uploaded_file is not None:
            import csv
            import io
            reader = csv.DictReader(io.StringIO(uploaded_file.getvalue().decode("utf-8")))
            imported = 0
            for row in reader:
                # Expect columns: Date, Amount, Category, Type, Notes, Tags
                try:
                    db.add_transaction(Transaction(
                        id=None,
                        date=row.get("Date", ""),
                        amount=float(row.get("Amount", 0)),
                        category=row.get("Category", ""),
                        type=row.get("Type", "expense"),
                        notes=row.get("Notes", None),
                        tags=row.get("Tags", None)
                    ))
                    imported += 1
                except Exception as e:
                    st.warning(f"Skipped row due to error: {e}")
            st.success(f"Imported {imported} transactions from CSV.")
        st.info("CSV columns: Date, Amount, Category, Type, Notes, Tags")
    elif report_type == "Monthly Summary":
        col1, col2 = st.columns(2)
        with col1:
            year = st.number_input("Year", 2020, 2030, datetime.now().year)
        with col2:
            month = st.number_input("Month", 1, 12, datetime.now().month)
        
        summary = service.get_month_summary(year, month)
        
        st.subheader(f"Summary for {year}-{month:02d}")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Income", f"${summary['total_income']:.2f}")
        with col2:
            st.metric("Total Expenses", f"${summary['total_expense']:.2f}")
        with col3:
            st.metric("Balance", f"${summary['balance']:.2f}")
        
        if summary['by_category']:
            st.subheader("By Category")
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(summary['by_category'].keys(), summary['by_category'].values(), color='#667eea')
            ax.set_ylabel("Amount ($)")
            ax.set_title(f"Expenses by Category - {year}-{month:02d}")
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig)
    
    elif report_type == "Monthly Comparison":
        col1, col2 = st.columns(2)
        with col1:
            year1 = st.number_input("Year 1", 2020, 2030, datetime.now().year)
            month1 = st.number_input("Month 1", 1, 12, datetime.now().month)
        with col2:
            year2 = st.number_input("Year 2", 2020, 2030, datetime.now().year)
            month2 = st.number_input("Month 2", 1, 12, datetime.now().month - 1 if datetime.now().month > 1 else 12)
        
        summary1 = service.get_month_summary(year1, month1)
        summary2 = service.get_month_summary(year2, month2)
        
        st.subheader(f"Comparison: {year1}-{month1:02d} vs {year2}-{month2:02d}")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(f"Income {year1}-{month1:02d}", f"${summary1['total_income']:.2f}")
        with col2:
            st.metric(f"Expense {year1}-{month1:02d}", f"${summary1['total_expense']:.2f}")
        with col3:
            st.metric(f"Income {year2}-{month2:02d}", f"${summary2['total_income']:.2f}")
        with col4:
            st.metric(f"Expense {year2}-{month2:02d}", f"${summary2['total_expense']:.2f}")
        
        # Comparison chart
        fig, ax = plt.subplots(figsize=(10, 5))
        months = [f"{year1}-{month1:02d}", f"{year2}-{month2:02d}"]
        expenses = [summary1['total_expense'], summary2['total_expense']]
        income = [summary1['total_income'], summary2['total_income']]
        
        x = range(len(months))
        width = 0.35
        ax.bar([i - width/2 for i in x], income, width, label='Income', color='#4caf50')
        ax.bar([i + width/2 for i in x], expenses, width, label='Expenses', color='#f44336')
        ax.set_ylabel("Amount ($)")
        ax.set_title("Monthly Comparison")
        ax.set_xticks(x)
        ax.set_xticklabels(months)
        ax.legend()
        st.pyplot(fig)
    
    elif report_type == "Savings Analysis":
        rec = service.get_savings_recommendation()
        
        st.subheader("💡 Savings Recommendation")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Income", f"${rec['total_income']:.2f}")
        with col2:
            st.metric("Total Expense", f"${rec['total_expense']:.2f}")
        with col3:
            st.metric("Current Balance", f"${rec['current_balance']:.2f}")
        
        st.info(f"Recommended Savings (20%): ${rec['recommended_savings']:.2f}")
        if rec['can_achieve']:
            st.success("✅ You can achieve the recommended savings goal!")
        else:
            st.warning("⚠️ You may need to reduce expenses to reach the savings goal.")
    
    elif report_type == "Prediction":
        pred = service.predict_next_month_expense()
        st.subheader("🔮 Next Month Expense Prediction")
        st.metric("Predicted Expense (Average)", f"${pred:.2f}")
        st.info("This is a simple prediction based on your average spending.")
    
    elif report_type == "Export Data":
        st.subheader("📥 Export Your Data")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Export as CSV", width='stretch'):
                if service.export_to_csv("expense_report.csv"):
                    with open("expense_report.csv", "rb") as f:
                        st.download_button(
                            label="Download CSV",
                            data=f.read(),
                            file_name="expense_report.csv",
                            mime="text/csv"
                        )
                    st.success("✅ CSV exported!")
        
        with col2:
            if st.button("Export as TXT", width='stretch'):
                if service.export_to_txt("expense_report.txt"):
                    with open("expense_report.txt", "r") as f:
                        st.download_button(
                            label="Download TXT",
                            data=f.read(),
                            file_name="expense_report.txt",
                            mime="text/plain"
                        )
                    st.success("✅ TXT exported!")


# === PAGE: BUDGET SETTINGS ===
elif page == "⚙️ Budget Settings":
    st.title("⚙️ Budget Settings")
    st.subheader("Set Category Budget Limits")

    categories = ["Food", "Transport", "Shopping", "Entertainment", "Utilities", "Health", "Other"]
    current_budgets = db.get_budgets()

    st.markdown("""
        <style>
        .budget-row { display: flex; align-items: center; margin-bottom: 1rem; }
        .budget-label { flex: 2; font-weight: 500; }
        .budget-input { flex: 2; margin-right: 1rem; }
        .budget-btn { flex: 1; }
        </style>
    """, unsafe_allow_html=True)

    for category in categories:
        cols = st.columns([2, 2, 1])
        with cols[0]:
            st.markdown(f"<div class='budget-label'>{category} Budget Limit ($)</div>", unsafe_allow_html=True)
        with cols[1]:
            current_limit = float(current_budgets.get(category, 0))
            limit = st.number_input(" ", min_value=0.0, step=0.01, value=current_limit, key=f"budget_{category}")
        with cols[2]:
            if st.button("Set", key=f"btn_{category}", width='stretch'):
                db.set_budget(category, limit)
                st.success(f"✅ {category} budget set to ${limit:.2f}")

    st.divider()
    st.subheader("Current Budgets")
    budgets = db.get_budgets()
    if budgets:
        df_budgets = []
        for cat, limit in budgets.items():
            df_budgets.append({"Category": cat, "Limit ($)": f"${limit:.2f}"})
        st.dataframe(pd.DataFrame(df_budgets), width='stretch')
    else:
        st.info("No budgets set yet.")


st.sidebar.divider()
st.sidebar.info("Smart Expense Tracker v1.0 - Python Course Project")
