#New Script

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
                st.success("Welcome back!")
                st.session_state.logged_in = True
    else:
        st.warning("Please enter both Name and Email.")

# If not logged in, stop execution
if not st.session_state.logged_in:
    st.stop()

else:
    # MAIN APP AFTER LOGIN
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

    if st.button("Calculate Ratios and Cash Flow"):
        # Liquidity Ratios
        current_ratio = current_assets / current_liabilities if current_liabilities != 0 else 0
        quick_ratio = (current_assets - inventory) / current_liabilities if current_liabilities != 0 else 0
        cash_ratio = cash / current_liabilities if current_liabilities != 0 else 0

        # Profitability Ratios
        gross_profit_margin = gross_profit / revenue if revenue != 0 else 0
        return_on_assets = net_income / total_assets if total_assets != 0 else 0
        return_on_equity = net_income / equity if equity != 0 else 0
        earnings_per_share = net_income / number_of_shares if number_of_shares != 0 else 0

        # Solvency
        debt_to_equity = total_liabilities / equity if equity != 0 else 0

        # Efficiency
        inventory_turnover = cost_of_goods_sold / average_inventory if average_inventory != 0 else 0

        # Cash Flow Calculations
        net_cash_flow = operating_cash_flow + investing_cash_flow + financing_cash_flow

        st.subheader("Calculated Ratios and Cash Flow")

        ratios_data = [
            {"Ratio": "Current Ratio", "Value": f"{current_ratio:.2f}",
             "Analysis": "Weak" if current_ratio < 2 else "Strong",
             "Implication": "Struggle to cover short-term debts" if current_ratio < 2 else "Can cover short-term debts comfortably",
             "Advice": "Increase liquid assets." if current_ratio < 2 else "Maintain current ratio."},

            {"Ratio": "Quick Ratio", "Value": f"{quick_ratio:.2f}",
             "Analysis": "Weak" if quick_ratio < 1 else "Strong",
             "Implication": "Insufficient liquid assets" if quick_ratio < 1 else "Sufficient quick assets",
             "Advice": "Increase cash or receivables." if quick_ratio < 1 else "Maintain quick ratio."},

            {"Ratio": "Cash Ratio", "Value": f"{cash_ratio:.2f}",
             "Analysis": "Low" if cash_ratio < 1 else "Strong",
             "Implication": "Limited immediate liquidity" if cash_ratio < 1 else "Good immediate liquidity",
             "Advice": "Boost cash reserves." if cash_ratio < 1 else "Maintain cash levels."},

            {"Ratio": "Debt-to-Equity", "Value": f"{debt_to_equity:.2f}",
             "Analysis": "High" if debt_to_equity > 2 else "Healthy",
             "Implication": "High leverage risk" if debt_to_equity > 2 else "Balanced capital structure",
             "Advice": "Reduce debts or increase equity." if debt_to_equity > 2 else "Maintain leverage."},

            {"Ratio": "Gross Profit Margin", "Value": f"{gross_profit_margin:.2f}",
             "Analysis": "Low" if gross_profit_margin < 0.3 else "Good",
             "Implication": "Thin profit margin" if gross_profit_margin < 0.3 else "Healthy profit margin",
             "Advice": "Increase sales or reduce costs." if gross_profit_margin < 0.3 else "Maintain margins."},

            {"Ratio": "Return on Assets (ROA)", "Value": f"{return_on_assets:.2f}",
             "Analysis": "Low" if return_on_assets < 0.05 else "Good",
             "Implication": "Inefficient asset use" if return_on_assets < 0.05 else "Efficient asset utilization",
             "Advice": "Improve operational efficiency." if return_on_assets < 0.05 else "Maintain efficiency."},

            {"Ratio": "Return on Equity (ROE)", "Value": f"{return_on_equity:.2f}",
             "Analysis": "Low" if return_on_equity < 0.1 else "Strong",
             "Implication": "Poor shareholder returns" if return_on_equity < 0.1 else "Good shareholder returns",
             "Advice": "Improve profitability." if return_on_equity < 0.1 else "Maintain profitability."},

            {"Ratio": "Earnings Per Share (EPS)", "Value": f"{earnings_per_share:.2f}",
             "Analysis": "Low" if earnings_per_share < 1 else "Strong",
             "Implication": "Low profitability per share" if earnings_per_share < 1 else "Good profitability per share",
             "Advice": "Grow net income or reduce share dilution." if earnings_per_share < 1 else "Maintain earnings growth."},

            {"Ratio": "Net Cash Flow", "Value": f"{net_cash_flow:.2f}",
             "Analysis": "Negative" if net_cash_flow < 0 else "Positive",
             "Implication": "Insufficient cash flow" if net_cash_flow < 0 else "Healthy cash flow",
             "Advice": "Improve operational cash flow." if net_cash_flow < 0 else "Maintain positive cash flow."}
        ]

        ratios_df = pd.DataFrame(ratios_data)
        st.dataframe(ratios_df)

        # CSV download
        csv = ratios_df.to_csv(index=False)
        st.download_button("Download Ratios and Cash Flow as CSV", csv, "financial_ratios_and_cashflow_analysis.csv", "text/csv")

    if not os.path.exists("results"):
        os.makedirs("results")