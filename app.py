import streamlit as st
import pandas as pd
import os
from datetime import datetime
from io import BytesIO

# Load user access CSV
USERS_CSV = "data/users.csv"

if not os.path.exists(USERS_CSV):
    df = pd.DataFrame(columns=["name", "email", "status", "trial_used", "last_action", "action_by"])
    df.to_csv(USERS_CSV, index=False)

users_df = pd.read_csv(USERS_CSV)

# Ensure new columns exist in old CSV
if 'last_action' not in users_df.columns:
    users_df['last_action'] = ''
if 'action_by' not in users_df.columns:
    users_df['action_by'] = ''
    users_df.to_csv(USERS_CSV, index=False)

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
            new_user = pd.DataFrame([[user_name, user_email, "pending", "no", "", ""]], 
                                    columns=["name", "email", "status", "trial_used", "last_action", "action_by"])
            users_df = pd.concat([users_df, new_user], ignore_index=True)
            save_users_df(users_df)
            st.success("Free trial granted. Enjoy your one-time access!")
            st.session_state.logged_in = True
            users_df.loc[users_df['email'] == user_email, 'trial_used'] = 'yes'
            save_users_df(users_df)
        else:
            status = user_record.iloc[0]['status']
            trial_used = user_record.iloc[0]['trial_used']

            if status == "authorized":
                st.success("Welcome back, authorized user!")
                st.session_state.logged_in = True
            elif status == "rejected":
                st.info("Your previous request was rejected — resetting to pending for reconsideration.")
                users_df.loc[users_df['email'] == user_email, 'status'] = 'pending'
                users_df.loc[users_df['email'] == user_email, 'last_action'] = datetime.now().strftime('%Y-%m-%d %H:%M')
                users_df.loc[users_df['email'] == user_email, 'action_by'] = user_name
                save_users_df(users_df)
                st.warning("Access pending admin approval.")
            elif trial_used == "no":
                st.success("Free trial granted. Enjoy your one-time access!")
                st.session_state.logged_in = True
                users_df.loc[users_df['email'] == user_email, 'trial_used'] = 'yes'
                save_users_df(users_df)
            else:
                st.warning("Access pending admin approval.")
    else:
        st.warning("Please enter both Name and Email.")

# If not logged in, stop execution
if not st.session_state.logged_in:
    st.stop()

# === ADMIN PANEL (SIDEBAR) ===
if user_name.strip().upper() == "ADEKUNLE ADEGBIE":
    st.sidebar.title("Admin Panel")
    st.sidebar.write("Manage pending user approvals:")

    pending_users = users_df[users_df['status'] == 'pending']
    if not pending_users.empty:
        for idx, row in pending_users.iterrows():
            st.sidebar.write(f"{row['name']} ({row['email']})")
            col1, col2 = st.sidebar.columns(2)
            with col1:
                if st.button("Approve", key=f"approve_{idx}"):
                    users_df.loc[users_df['email'] == row['email'], 'status'] = 'authorized'
                    users_df.loc[users_df['email'] == row['email'], 'last_action'] = datetime.now().strftime('%Y-%m-%d %H:%M')
                    users_df.loc[users_df['email'] == row['email'], 'action_by'] = user_name
                    save_users_df(users_df)
                    st.rerun()
            with col2:
                if st.button("Reject", key=f"reject_{idx}"):
                    users_df.loc[users_df['email'] == row['email'], 'status'] = 'rejected'
                    users_df.loc[users_df['email'] == row['email'], 'last_action'] = datetime.now().strftime('%Y-%m-%d %H:%M')
                    users_df.loc[users_df['email'] == row['email'], 'action_by'] = user_name
                    save_users_df(users_df)
                    st.rerun()
    else:
        st.sidebar.write("No pending users.")

# === MAIN APP ===
st.title("📊 Financial Ratio Analysis App")
st.write(f"Hello **{user_name}** — your email: {user_email}")

st.markdown("""
    <style>
    .main { background-color: #f5f7fa; }
    .block-container { padding-top: 2rem; }
    .stButton>button { background-color: #4CAF50; color: white; border-radius: 5px; }
    .stButton>button:hover { background-color: #45a049; }
    </style>
    """, unsafe_allow_html=True)

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

st.subheader("Per Share Data")
number_of_shares = st.number_input("Number of Shares Outstanding", min_value=0.0)

# Cash Flow Inputs
st.subheader("Cash Flow Statement")
operating_cash_flow = st.number_input("Operating Cash Flow")
investing_cash_flow = st.number_input("Investing Cash Flow")
financing_cash_flow = st.number_input("Financing Cash Flow")

# Compute ratios and display
if st.button("Calculate Ratios and Cash Flow"):
    ratios_data = []

    if current_liabilities != 0:
        ratios_data.append({
            "Ratio": "Current Ratio",
            "Value": f"{current_assets/current_liabilities:.2f}"
        })
        ratios_data.append({
            "Ratio": "Quick Ratio",
            "Value": f"{(current_assets-inventory)/current_liabilities:.2f}"
        })
        ratios_data.append({
            "Ratio": "Cash Ratio",
            "Value": f"{cash/current_liabilities:.2f}"
        })

    if equity != 0:
        ratios_data.append({
            "Ratio": "Debt-to-Equity",
            "Value": f"{total_liabilities/equity:.2f}"
        })

    if revenue != 0:
        ratios_data.append({
            "Ratio": "Net Profit Margin",
            "Value": f"{(net_income/revenue)*100:.2f}%"
        })

    if total_assets != 0:
        ratios_data.append({
            "Ratio": "Return on Assets (ROA)",
            "Value": f"{(net_income/total_assets)*100:.2f}%"
        })

    if equity != 0:
        ratios_data.append({
            "Ratio": "Return on Equity (ROE)",
            "Value": f"{(net_income/equity)*100:.2f}%"
        })

    if number_of_shares != 0:
        ratios_data.append({
            "Ratio": "Earnings Per Share (EPS)",
            "Value": f"{net_income/number_of_shares:.2f}"
        })

    # Show results
    st.subheader("Calculated Ratios")
    ratios_df = pd.DataFrame(ratios_data)
    st.dataframe(ratios_df)

    # Allow download
    output = BytesIO()
    ratios_df.to_csv(output, index=False)
    st.download_button("Download Ratios CSV", data=output.getvalue(), file_name="financial_ratios.csv", mime="text/csv")
