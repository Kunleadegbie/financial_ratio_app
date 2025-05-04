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
if 'approved' not in users_df.columns:
    users_df['approved'] = 'no'

def save_users_df(df):
    df.to_csv(USERS_CSV, index=False)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Sidebar login
st.sidebar.title("Login")
user_name = st.sidebar.text_input("Enter your Name and Surname")
user_email = st.sidebar.text_input("Enter your Email")
login_button = st.sidebar.button("Login")

# Login process
if login_button:
    if user_name and user_email:
        user_record = users_df[users_df['email'] == user_email]

        if user_record.empty:
            new_user = pd.DataFrame([[user_name, user_email, "pending", "no", "no"]], columns=["name", "email", "status", "trial_used", "approved"])
            users_df = pd.concat([users_df, new_user], ignore_index=True)
            save_users_df(users_df)
            st.success("Free trial granted.")
            st.session_state.logged_in = True
            users_df.loc[users_df['email'] == user_email, 'trial_used'] = 'yes'
            save_users_df(users_df)
        else:
            trial_used = user_record.iloc[0]['trial_used']
            approved = user_record.iloc[0]['approved']

            if trial_used == "no":
                st.success("Free trial granted.")
                st.session_state.logged_in = True
                users_df.loc[users_df['email'] == user_email, 'trial_used'] = 'yes'
                save_users_df(users_df)
            elif trial_used == "yes" and approved == "no":
                st.warning("Trial used. Await admin approval.")
                st.session_state.logged_in = False
            elif trial_used == "yes" and approved == "yes":
                st.success("Welcome back. Approved.")
                st.session_state.logged_in = True
    else:
        st.warning("Enter both Name and Email.")

def check_access(email):
    record = users_df[users_df['email'] == email]
    if not record.empty and record.iloc[0]['trial_used'] == "yes" and record.iloc[0]['approved'] == "no":
        st.warning("Trial used. Contact admin.")
        st.stop()

# Admin section
if user_email == "kadegbie@gmail.com":
    st.subheader("Admin Panel")
    pending_users = users_df[(users_df['trial_used'] == 'yes') & (users_df['approved'] == 'no')]

    if not pending_users.empty:
        st.write("Pending Approvals")
        st.dataframe(pending_users[['name', 'email']])

        approve_emails = st.text_area("Emails to Approve (comma-separated)").strip()
        deny_emails = st.text_area("Emails to Deny (comma-separated)").strip()

        if st.button("Process"):
            if approve_emails:
                approve_list = [email.strip() for email in approve_emails.split(",") if email.strip()]
                users_df.loc[users_df['email'].isin(approve_list), 'approved'] = 'yes'
                st.success(f"Approved: {', '.join(approve_list)}")

            if deny_emails:
                deny_list = [email.strip() for email in deny_emails.split(",") if email.strip()]
                users_df.loc[users_df['email'].isin(deny_list), 'approved'] = 'no'
                st.info(f"Denied: {', '.join(deny_list)}")

            save_users_df(users_df)
    else:
        st.write("No pending approvals.")

if not st.session_state.logged_in:
    st.stop()

check_access(user_email)

# Financial Calculator App
st.title("📊 Financial Ratio Calculator")

# Financial Inputs
st.header("Enter Financial Figures")
company = st.text_input("Company Name (optional)")

current_assets = st.number_input("Current Assets", min_value=0.0, value=0.0)
current_liabilities = st.number_input("Current Liabilities", min_value=0.0, value=0.0)
inventory = st.number_input("Inventory", min_value=0.0, value=0.0)
cash = st.number_input("Cash & Equivalents", min_value=0.0, value=0.0)
gross_profit = st.number_input("Gross Profit", min_value=0.0, value=0.0)
net_income = st.number_input("Net Income", min_value=0.0, value=0.0)
revenue = st.number_input("Revenue", min_value=0.0, value=0.0)
total_assets = st.number_input("Total Assets", min_value=0.0, value=0.0)
equity = st.number_input("Equity", min_value=0.0, value=0.0)
total_liabilities = st.number_input("Total Liabilities", min_value=0.0, value=0.0)
number_of_shares = st.number_input("Number of Shares", min_value=0.0, value=0.0)
operating_cash_flow = st.number_input("Operating Cash Flow", value=0.0)
investing_cash_flow = st.number_input("Investing Cash Flow", value=0.0)
financing_cash_flow = st.number_input("Financing Cash Flow", value=0.0)

if st.button("Calculate"):
    result_data = []
    net_cash_flow = operating_cash_flow + investing_cash_flow + financing_cash_flow

    if current_assets and current_liabilities:
        current_ratio = current_assets / current_liabilities
        result_data.append(["Current Ratio", round(current_ratio, 2), "Weak", "Struggle to cover short-term debts", "Increase liquid assets."])

    if (current_assets - inventory) and current_liabilities:
        quick_ratio = (current_assets - inventory) / current_liabilities
        result_data.append(["Quick Ratio", round(quick_ratio, 2), "Weak", "Insufficient liquid assets", "Increase cash or receivables."])

    if cash and current_liabilities:
        cash_ratio = cash / current_liabilities
        result_data.append(["Cash Ratio", round(cash_ratio, 2), "Low", "Limited immediate liquidity", "Boost cash reserves."])

    if total_liabilities and equity:
        debt_equity = total_liabilities / equity
        result_data.append(["Debt-to-Equity", round(debt_equity, 2), "Healthy", "Balanced capital structure", "Maintain leverage."])

    if gross_profit and revenue:
        gross_margin = gross_profit / revenue
        result_data.append(["Gross Profit Margin", round(gross_margin, 2), "Good", "Healthy profit margin", "Maintain margins."])

    if net_income and total_assets:
        roa = net_income / total_assets
        result_data.append(["Return on Assets (ROA)", round(roa, 2), "Good", "Efficient asset use", "Maintain efficiency."])

    if net_income and equity:
        roe = net_income / equity
        result_data.append(["Return on Equity (ROE)", round(roe, 2), "Strong", "Good shareholder returns", "Maintain profitability."])

    if net_income and number_of_shares:
        eps = net_income / number_of_shares
        result_data.append(["Earnings Per Share (EPS)", round(eps, 2), "Low", "Low profit per share", "Grow net income or reduce dilution."])

    result_data.append(["Net Cash Flow", round(net_cash_flow, 2), "Positive" if net_cash_flow > 0 else "Negative", 
                        "Healthy cash flow" if net_cash_flow > 0 else "Cash flow issues", 
                        "Maintain positive cash flow" if net_cash_flow > 0 else "Improve cash flow management"])

    # Convert to DataFrame
    result_df = pd.DataFrame(result_data, columns=["Ratio", "Value", "Analysis", "Implication", "Advice"])
    st.dataframe(result_df)

    csv = result_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Results as CSV", data=csv, file_name=f"{company}_financial_ratios.csv", mime="text/csv")

