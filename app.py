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
                st.error("Access denied. Please contact admin for authorization.")
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
            background-color: #1a73e8;
            color: white;
            border-radius: 5px;
        }
        .stButton>button:hover {
            background-color: #155ab6;
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

    # Calculating financial ratios
    current_ratio = current_assets / current_liabilities if current_liabilities != 0 else 0
    quick_ratio = (current_assets - inventory) / current_liabilities if current_liabilities != 0 else 0
    cash_ratio = cash / current_liabilities if current_liabilities != 0 else 0

    # Analyzing the results
    results = {
        "Ratio": ["Current Ratio", "Quick Ratio", "Cash Ratio"],
        "Value": [current_ratio, quick_ratio, cash_ratio],
        "Analysis": [
            "Weak" if current_ratio < 1 else "Strong",
            "Weak" if quick_ratio < 1 else "Strong",
            "Low" if cash_ratio < 0.5 else "High"
        ],
        "Implication": [
            "Struggle to cover short-term debts" if current_ratio < 1 else "Able to cover short-term debts",
            "Insufficient liquid assets" if quick_ratio < 1 else "Sufficient liquidity",
            "Limited immediate liquidity" if cash_ratio < 0.5 else "Strong liquidity position"
        ],
        "Advice": [
            "Increase liquid assets." if current_ratio < 1 else "Maintain current asset levels.",
            "Increase cash or receivables." if quick_ratio < 1 else "Optimize current asset management.",
            "Boost cash reserves." if cash_ratio < 0.5 else "Maintain cash reserves."
        ]
    }

    # Creating a DataFrame for results
    df_results = pd.DataFrame(results)

    # Display the results
    st.write(df_results)

    # Creating download option for CSV file
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    csv_file = convert_df_to_csv(df_results)

    # Download button
    st.download_button(
        label="Download Financial Ratios Report",
        data=csv_file,
        file_name=f"financial_ratios_{user_email}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv",
        mime="text/csv"
    )
    
    # Create results directory if it doesn't exist
    if not os.path.exists("results"):
        os.makedirs("results")
