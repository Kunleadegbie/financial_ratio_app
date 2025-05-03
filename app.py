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

    # Custom CSS for clean styling
    st.markdown("""
        <style>
        .main {
            background-color: #f5f7fa;
        }
        .block-container {
            padding-top: 2rem;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 5px;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        </style>
        """, unsafe_allow_html=True)

    # Title and input sections
    st.title("CHUMCRED ACADEMY Financial Ratio Calculator")
    st.header("Enter Financial Figures")
    company = st.text_input("Company Name (optional)")

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

    # Calculation button
    if st.button("Calculate Ratios"):
        # Example ratios calculation
        liquidity_ratio = current_assets / current_liabilities if current_liabilities != 0 else 0
        profitability_ratio = gross_profit / revenue if revenue != 0 else 0
        solvency_ratio = total_liabilities / equity if equity != 0 else 0
        efficiency_ratio = cost_of_goods_sold / average_inventory if average_inventory != 0 else 0

        # Display the results
        st.subheader("Calculated Ratios")
        st.write(f"Liquidity Ratio: {liquidity_ratio:.2f}")
        st.write(f"Profitability Ratio: {profitability_ratio:.2f}")
        st.write(f"Solvency Ratio: {solvency_ratio:.2f}")
        st.write(f"Efficiency Ratio: {efficiency_ratio:.2f}")

        # Prepare data for CSV download
        results = {
            "Liquidity Ratio": liquidity_ratio,
            "Profitability Ratio": profitability_ratio,
            "Solvency Ratio": solvency_ratio,
            "Efficiency Ratio": efficiency_ratio
        }
        results_df = pd.DataFrame([results])

        csv = results_df.to_csv(index=False)
        st.download_button("Download Results as CSV", csv, "financial_ratios.csv", "text/csv")

        # 🚀 Liquidity Ratios Detailed Analysis
        st.subheader("Liquidity Ratios Detailed Analysis")

        current_ratio = current_assets / current_liabilities if current_liabilities != 0 else 0
        quick_ratio = (current_assets - inventory) / current_liabilities if current_liabilities != 0 else 0
        cash_ratio = cash / current_liabilities if current_liabilities != 0 else 0

        analysis_data = [
            {
                "Ratio": "Current Ratio",
                "Value": f"{current_ratio:.2f}",
                "Analysis": "Weak" if current_ratio < 2 else "Healthy",
                "Implication": "Struggle to cover short-term debts" if current_ratio < 2 else "Can cover short-term obligations",
                "Advice": "Increase liquid assets." if current_ratio < 2 else "Maintain current liquidity."
            },
            {
                "Ratio": "Quick Ratio",
                "Value": f"{quick_ratio:.2f}",
                "Analysis": "Weak" if quick_ratio < 1 else "Healthy",
                "Implication": "Insufficient liquid assets" if quick_ratio < 1 else "Adequate quick liquidity",
                "Advice": "Increase cash or receivables." if quick_ratio < 1 else "Good liquidity management."
            },
            {
                "Ratio": "Cash Ratio",
                "Value": f"{cash_ratio:.2f}",
                "Analysis": "Low" if cash_ratio < 0.5 else "Adequate",
                "Implication": "Limited immediate liquidity" if cash_ratio < 0.5 else "Sufficient immediate liquidity",
                "Advice": "Boost cash reserves." if cash_ratio < 0.5 else "Maintain cash position."
            }
        ]

        liquidity_df = pd.DataFrame(analysis_data)

        st.dataframe(liquidity_df)

        # Download button for Liquidity Analysis
        liquidity_csv = liquidity_df.to_csv(index=False)
        st.download_button("Download Liquidity Analysis as CSV", liquidity_csv, "liquidity_analysis.csv", "text/csv")

    # Create results directory if it doesn't exist
    if not os.path.exists("results"):
        os.makedirs("results")
