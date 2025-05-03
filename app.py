import streamlit as st
import pandas as pd
import os

# Load user access CSV
USERS_CSV = "data/users.csv"

if not os.path.exists(USERS_CSV):
    df = pd.DataFrame(columns=["name", "email", "status", "trial_used", "approved"])
    df.to_csv(USERS_CSV, index=False)

users_df = pd.read_csv(USERS_CSV)

# Ensure 'approved' column exists
def ensure_columns_exist(users_df):
    if 'approved' not in users_df.columns:
        users_df['approved'] = 'no'

# Ensure the column exists
ensure_columns_exist(users_df)

# User login inputs
st.sidebar.title("Login")
user_name = st.sidebar.text_input("Enter your Name and Surname")
user_email = st.sidebar.text_input("Enter your Email")
login_button = st.sidebar.button("Login")

def save_users_df(df):
    df.to_csv(USERS_CSV, index=False)

# Session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if login_button:
    if user_name and user_email:
        user_record = users_df[users_df['email'] == user_email]

        if user_record.empty:
            new_user = pd.DataFrame([[user_name, user_email, "pending", "no", "no"]], columns=["name", "email", "status", "trial_used", "approved"])
            users_df = pd.concat([users_df, new_user], ignore_index=True)
            save_users_df(users_df)
            st.success("Free trial granted. Enjoy your one-time access!")
            st.session_state.logged_in = True
            users_df.loc[users_df['email'] == user_email, 'trial_used'] = 'yes'
            save_users_df(users_df)
        else:
            status = user_record.iloc[0]['status']
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
            else:
                st.success("Welcome back! You have already used your free trial.")
                st.session_state.logged_in = True
    else:
        st.warning("Please enter both Name and Email.")

# Admin Section (Visible to admin only)
if user_email == "kadegbie@gmail.com":
    st.subheader("Admin Section")
    st.write("This section is for admin use only.")

    # Show list of graded-out emails for admin to approve
    graded_out_users = users_df[users_df['trial_used'] == 'yes']
    graded_out_users = graded_out_users[graded_out_users['approved'] == 'no']
    
    if not graded_out_users.empty:
        st.write("Emails that need approval:")
        st.dataframe(graded_out_users[['name', 'email']])

        approved_email = st.text_input("Enter email to approve")
        if st.button("Approve Email"):
            if approved_email in graded_out_users['email'].values:
                users_df.loc[users_df['email'] == approved_email, 'approved'] = 'yes'
                save_users_df(users_df)
                st.success(f"Email {approved_email} has been approved!")
            else:
                st.warning("This email is not in the graded-out list.")
    else:
        st.write("No emails pending approval.")

# If not logged in, stop execution
if not st.session_state.logged_in:
    st.stop()

else:
    # MAIN APP AFTER LOGIN
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

    # Cash Flow Inputs
    st.subheader("Cash Flow Statement")
    operating_cash_flow = st.number_input("Operating Cash Flow")
    investing_cash_flow = st.number_input("Investing Cash Flow")
    financing_cash_flow = st.number_input("Financing Cash Flow")

    # Disable input if the user has already used their free trial and is not approved by admin
    if trial_used == "yes" and approved == "no":
        st.warning("You cannot use the Financial Ratio Calculator again. Please contact the admin for approval.")
        st.stop()

    if st.button("Calculate Ratios and Cash Flow"):
        # Ratios and Cash Flow Calculations
        net_cash_flow = operating_cash_flow + investing_cash_flow + financing_cash_flow

        # Display results
        st.subheader("Calculated Ratios and Cash Flow")

        st.write(f"Net Cash Flow: {net_cash_flow:.2f}")
