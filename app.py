import streamlit as st
import pandas as pd
import os
from datetime import datetime
from io import BytesIO

# Load user access CSV
USERS_CSV = "data/users.csv"

if not os.path.exists(USERS_CSV):
    df = pd.DataFrame(columns=["name", "email", "status", "trial_used"])
    df.to_csv(USERS_CSV, index=False)

users_df = pd.read_csv(USERS_CSV)

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
            new_user = pd.DataFrame([[user_name, user_email, "pending", "no"]], columns=["name", "email", "status", "trial_used"])
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
                    save_users_df(users_df)
                    st.rerun()
            with col2:
                if st.button("Reject", key=f"reject_{idx}"):
                    users_df.loc[users_df['email'] == row['email'], 'status'] = 'rejected'
                    save_users_df(users_df)
                    st.experimental_rerun()
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

if st.button("Calculate Ratios and Cash Flow"):
    ratios_data = []

    if current_liabilities != 0:
        ratios_data.append({
            "Ratio": "Current Ratio",
            "Value": f"{current_assets/current_liabilities:.2f}",
            "Analysis": "Weak" if current_assets/current_liabilities < 2 else "Strong",
            "Implication": "Struggle to cover short-term debts" if current_assets/current_liabilities < 2 else "Can cover short-term debts comfortably",
            "Advice": "Increase liquid assets." if current_assets/current_liabilities < 2 else "Maintain current ratio."
        })
        ratios_data.append({
            "Ratio": "Quick Ratio",
            "Value": f"{(current_assets-inventory)/current_liabilities:.2f}",
            "Analysis": "Weak" if (current_assets-inventory)/current_liabilities < 1 else "Strong",
            "Implication": "Insufficient liquid assets" if (current_assets-inventory)/current_liabilities < 1 else "Sufficient quick assets",
            "Advice": "Increase cash or receivables." if (current_assets-inventory)/current_liabilities < 1 else "Maintain quick ratio."
        })
        ratios_data.append({
            "Ratio": "Cash Ratio",
            "Value": f"{cash/current_liabilities:.2f}",
            "Analysis": "Low" if cash/current_liabilities < 1 else "Strong",
            "Implication": "Limited immediate liquidity" if cash/current_liabilities < 1 else "Good immediate liquidity",
            "Advice": "Boost cash reserves." if cash/current_liabilities < 1 else "Maintain cash levels."
        })

    if equity != 0:
        ratios_data.append({
            "Ratio": "Debt-to-Equity",
            "Value": f"{total_liabilities/equity:.2f}",
            "Analysis": "Healthy" if total_liabilities/equity <= 2 else "Risky",
            "Implication": "Balanced capital structure" if total_liabilities/equity <= 2 else "High leverage risk",
            "Advice": "Maintain leverage." if total_liabilities/equity <= 2 else "Reduce debt levels."
        })

    if revenue != 0:
        ratios_data.append({
            "Ratio": "Gross Profit Margin",
            "Value": f"{gross_profit/revenue:.2f}",
            "Analysis": "Good" if gross_profit/revenue >= 0.4 else "Weak",
            "Implication": "Healthy profit margin" if gross_profit/revenue >= 0.4 else "Low profitability",
            "Advice": "Maintain margins." if gross_profit/revenue >= 0.4 else "Improve cost control."
        })

    if total_assets != 0:
        ratios_data.append({
            "Ratio": "Return on Assets (ROA)",
            "Value": f"{net_income/total_assets:.2f}",
            "Analysis": "Good" if net_income/total_assets >= 0.15 else "Weak",
            "Implication": "Efficient asset utilization" if net_income/total_assets >= 0.15 else "Underperforming assets",
            "Advice": "Maintain efficiency." if net_income/total_assets >= 0.15 else "Improve asset utilization."
        })

    if equity != 0:
        ratios_data.append({
            "Ratio": "Return on Equity (ROE)",
            "Value": f"{net_income/equity:.2f}",
            "Analysis": "Strong" if net_income/equity >= 0.3 else "Low",
            "Implication": "Good shareholder returns" if net_income/equity >= 0.3 else "Weak returns",
            "Advice": "Maintain profitability." if net_income/equity >= 0.3 else "Improve earnings."
        })

    if number_of_shares != 0:
        ratios_data.append({
            "Ratio": "Earnings Per Share (EPS)",
            "Value": f"{net_income/number_of_shares:.2f}",
            "Analysis": "Low" if net_income/number_of_shares < 1 else "Good",
            "Implication": "Low profitability per share" if net_income/number_of_shares < 1 else "Healthy earnings per share",
            "Advice": "Grow net income or reduce share dilution." if net_income/number_of_shares < 1 else "Maintain EPS."
        })

    net_cash_flow = operating_cash_flow + investing_cash_flow + financing_cash_flow
    ratios_data.append({
        "Ratio": "Net Cash Flow",
        "Value": f"{net_cash_flow:,.2f}",
        "Analysis": "Positive" if net_cash_flow >= 0 else "Negative",
        "Implication": "Healthy cash flow" if net_cash_flow >= 0 else "Cash outflow issue",
        "Advice": "Maintain positive cash flow." if net_cash_flow >= 0 else "Control expenses and increase inflow."
    })

    ratios_df = pd.DataFrame(ratios_data)
    st.dataframe(ratios_df)

    # Download CSV
    csv_buffer = BytesIO()
    ratios_df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="Download Results as CSV",
        data=csv_buffer.getvalue(),
        file_name=f"{company or 'financial_ratios'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
