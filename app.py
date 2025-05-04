#latest script

import streamlit as st
import pandas as pd
import os

# Path to user data CSV
USERS_CSV = "data/users.csv"

# Initialize user CSV if it doesn't exist
if not os.path.exists(USERS_CSV):
    df = pd.DataFrame(columns=["name", "email", "status", "trial_used", "approved"])
    df.to_csv(USERS_CSV, index=False)

# Load users dataframe
users_df = pd.read_csv(USERS_CSV)

# Ensure 'approved' column exists
def ensure_columns_exist(df):
    if 'approved' not in df.columns:
        df['approved'] = 'no'

ensure_columns_exist(users_df)

# Save users dataframe
def save_users_df(df):
    df.to_csv(USERS_CSV, index=False)

# Session state for login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Sidebar Login Inputs
st.sidebar.title("Login")
user_name = st.sidebar.text_input("Enter your Name and Surname")
user_email = st.sidebar.text_input("Enter your Email")
login_button = st.sidebar.button("Login")

# Login process
if login_button:
    if user_name and user_email:
        user_record = users_df[users_df['email'] == user_email]

        if user_record.empty:
            # New user — first time
            new_user = pd.DataFrame([[user_name, user_email, "pending", "no", "no"]], columns=["name", "email", "status", "trial_used", "approved"])
            users_df = pd.concat([users_df, new_user], ignore_index=True)
            save_users_df(users_df)
            st.success("Free trial granted. Enjoy your one-time access!")
            st.session_state.logged_in = True
            users_df.loc[users_df['email'] == user_email, 'trial_used'] = 'yes'
            save_users_df(users_df)
        else:
            trial_used = user_record.iloc[0]['trial_used']
            approved = user_record.iloc[0]['approved']

            if trial_used == "no":
                st.success("Free trial granted. Enjoy your one-time access!")
                st.session_state.logged_in = True
                users_df.loc[users_df['email'] == user_email, 'trial_used'] = 'yes'
                save_users_df(users_df)
            elif trial_used == "yes" and approved == "no":
                st.warning("You have already used your free trial. Please contact the admin for approval.")
                st.session_state.logged_in = False
            elif trial_used == "yes" and approved == "yes":
                st.success("Welcome back! Admin has approved your continued access.")
                st.session_state.logged_in = True
    else:
        st.warning("Please enter both Name and Email.")

# Function to restrict access if trial used but not approved
def check_access(email):
    record = users_df[users_df['email'] == email]
    if not record.empty and record.iloc[0]['trial_used'] == "yes" and record.iloc[0]['approved'] == "no":
        st.warning("You cannot use the Financial Ratio Calculator again. Please contact the admin for approval.")
        st.stop()

# Admin Section
if user_email == "kadegbie@gmail.com":
    st.subheader("Admin Section")
    st.write("This section is for admin use only.")

    pending_users = users_df[(users_df['trial_used'] == 'yes') & (users_df['approved'] == 'no')]

    if not pending_users.empty:
        st.write("Emails needing approval:")
        st.dataframe(pending_users[['name', 'email']])

        approved_email = st.text_input("Enter email to approve")
        if st.button("Approve Email"):
            if approved_email in pending_users['email'].values:
                users_df.loc[users_df['email'] == approved_email, 'approved'] = 'yes'
                save_users_df(users_df)
                st.success(f"Email {approved_email} has been approved!")
            else:
                st.warning("This email is not in the pending list.")
    else:
        st.write("No emails pending approval.")

# Stop execution if not logged in
if not st.session_state.logged_in:
    st.stop()

# Check user access before showing main app
check_access(user_email)

# MAIN APP — Financial Ratio Calculator
st.title("📊 Financial Ratio Analysis App")
st.write(f"Hello **{user_name}** — your email: {user_email}")

st.title("CHUMCRED ACADEMY Financial Ratio Calculator")
st.header("Enter Financial Figures")
company = st.text_input("Company Name (optional)")

# Financial Ratios Inputs
st.subheader("Liquidity Ratios")
current_assets = st.number_input("Current Assets", min_value=0.0)
current_liabilities = st.number_input("Current Liabilities", min_value=0.0)
inventory = st.number_input("Inventory", min_value=0.0)
cash = st.number_input("Cash & Cash Equivalents", min_value=0.0)

st.subheader("Profitability Ratios")
gross_profit = st.number_input("Gross Profit", min_value=0.0)
net_income = st.number_input("Net Income", min_value=0.0)
revenue = st.number_input("Revenue", min_value=0.0)
total_assets = st.number_input("Total Assets", min_value=0.0)
equity = st.number_input("Equity", min_value=0.0)
operating_profit = st.number_input("Operating Profit", min_value=0.0)

st.subheader("Solvency Ratios")
total_liabilities = st.number_input("Total Liabilities", min_value=0.0)
interest_expense = st.number_input("Interest Expense", min_value=0.0)

st.subheader("Efficiency Ratios")
cost_of_goods_sold = st.number_input("Cost of Goods Sold", min_value=0.0)
average_inventory = st.number_input("Average Inventory", min_value=0.0)
accounts_receivable = st.number_input("Accounts Receivable", min_value=0.0)
average_receivable = st.number_input("Average Accounts Receivable", min_value=0.0)
average_payable = st.number_input("Average Accounts Payable", min_value=0.0)
accounts_payable = st.number_input("Accounts Payable", min_value=0.0)

st.subheader("Per Share Data")
number_of_shares = st.number_input("Number of Shares Outstanding", min_value=0.0)

st.subheader("Cash Flow Statement")
operating_cash_flow = st.number_input("Operating Cash Flow", value=0.0)
investing_cash_flow = st.number_input("Investing Cash Flow", value=0.0)
financing_cash_flow = st.number_input("Financing Cash Flow", value=0.0)

# Calculate and Display Ratios and Cash Flow
if st.button("Calculate Ratios and Cash Flow"):
    net_cash_flow = operating_cash_flow + investing_cash_flow + financing_cash_flow

    # Calculate Ratios
    current_ratio = current_assets / current_liabilities if current_liabilities else 0
    quick_ratio = (current_assets - inventory) / current_liabilities if current_liabilities else 0
    cash_ratio = cash / current_liabilities if current_liabilities else 0
    debt_to_equity = total_liabilities / equity if equity else 0
    gross_profit_margin = gross_profit / revenue if revenue else 0
    return_on_assets = net_income / total_assets if total_assets else 0
    return_on_equity = net_income / equity if equity else 0
    earnings_per_share = net_income / number_of_shares if number_of_shares else 0

    # Results Table Data
    results_data = [
        ["Current Ratio", round(current_ratio, 2), "Weak", "Struggle to cover short-term debts", "Increase liquid assets."],
        ["Quick Ratio", round(quick_ratio, 2), "Weak", "Insufficient liquid assets", "Increase cash or receivables."],
        ["Cash Ratio", round(cash_ratio, 2), "Low", "Limited immediate liquidity", "Boost cash reserves."],
        ["Debt-to-Equity", round(debt_to_equity, 2), "Healthy", "Balanced capital structure", "Maintain leverage."],
        ["Gross Profit Margin", round(gross_profit_margin, 2), "Good", "Healthy profit margin", "Maintain margins."],
        ["Return on Assets (ROA)", round(return_on_assets, 2), "Good", "Efficient asset utilization", "Maintain efficiency."],
        ["Return on Equity (ROE)", round(return_on_equity, 2), "Strong", "Good shareholder returns", "Maintain profitability."],
        ["Earnings Per Share (EPS)", round(earnings_per_share, 2), "Low", "Low profitability per share", "Grow net income or reduce share dilution."],
        ["Net Cash Flow", f"{net_cash_flow:,.2f}", "Positive", "Healthy cash flow", "Maintain positive cash flow."]
    ]

    results_df = pd.DataFrame(results_data, columns=["Ratio", "Value", "Analysis", "Implication", "Advice"])
    st.subheader("📊 Financial Ratio & Cash Flow Results")
    st.dataframe(results_df, use_container_width=True)
