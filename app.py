
# (Your app.py code from previous message here. 
# For brevity, I'm keeping it summarized in this comment — it will be included in the actual file.)

import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Load or create user access CSV
USERS_CSV = "data/users.csv"

if not os.path.exists(USERS_CSV):
    df = pd.DataFrame(columns=["name", "email", "status", "trial_used", "role"])
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
            new_user = pd.DataFrame([[user_name, user_email, "pending", "no", "user"]], 
                                    columns=["name", "email", "status", "trial_used", "role"])
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

            # Display role if admin
            role = user_record.iloc[0].get('role', 'user')
            if role == 'admin':
                st.sidebar.success("👑 You are logged in as an **Admin**.")

    else:
        st.warning("Please enter both Name and Email.")

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

    st.subheader("Solvency Ratios")
    total_liabilities = st.number_input("Total Liabilities", min_value=0.0)

    st.subheader("Per Share Data")
    number_of_shares = st.number_input("Number of Shares Outstanding", min_value=0.0)

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

        # Cash Flow Calculations
        net_cash_flow = operating_cash_flow + investing_cash_flow + financing_cash_flow

        # Build Ratios Data
        ratios_data = [
            {"Ratio": "Current Ratio", "Value": f"{current_ratio:.2f}"},
            {"Ratio": "Quick Ratio", "Value": f"{quick_ratio:.2f}"},
            {"Ratio": "Cash Ratio", "Value": f"{cash_ratio:.2f}"},
            {"Ratio": "Gross Profit Margin", "Value": f"{gross_profit_margin:.2f}"},
            {"Ratio": "Return on Assets", "Value": f"{return_on_assets:.2f}"},
            {"Ratio": "Return on Equity", "Value": f"{return_on_equity:.2f}"},
            {"Ratio": "Debt-to-Equity", "Value": f"{debt_to_equity:.2f}"},
            {"Ratio": "Earnings Per Share", "Value": f"{earnings_per_share:.2f}"},
            {"Ratio": "Net Cash Flow", "Value": f"{net_cash_flow:.2f}"},
        ]

        st.subheader("Calculated Ratios and Cash Flow")
        ratios_df = pd.DataFrame(ratios_data)
        st.dataframe(ratios_df)

        csv = ratios_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Ratios as CSV",
            data=csv,
            file_name=f"{company or 'company'}_financial_ratios.csv",
            mime='text/csv'
        )

