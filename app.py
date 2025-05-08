import streamlit as st
import pandas as pd
import datetime
from io import BytesIO

# App config
st.set_page_config(page_title="📊 Financial Ratio & Cash Flow Calculator", page_icon="📊", layout="centered")

# User database (in a real app, use a database)
if 'users' not in st.session_state:
    st.session_state.users = {'admin': {'password': '12345', 'approved': True}}  # admin user

if 'free_trial_log' not in st.session_state:
    st.session_state.free_trial_log = {}

# Authentication
st.sidebar.title("🔐 Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
login_button = st.sidebar.button("Login")

user_authenticated = False
is_admin = False

if login_button:
    if username in st.session_state.users:
        if st.session_state.users[username]['password'] == password:
            if st.session_state.users[username]['approved']:
                st.sidebar.success(f"Welcome {username}!")
                user_authenticated = True
                if username == 'admin':
                    is_admin = True
            else:
                st.sidebar.warning("Awaiting admin approval.")
        else:
            st.sidebar.error("Incorrect password.")
    else:
        # Free trial logic
        if username not in st.session_state.free_trial_log:
            st.session_state.free_trial_log[username] = {'used': True}
            st.session_state.users[username] = {'password': password, 'approved': True}  # Allow first time login
            st.sidebar.success(f"Free trial granted. Welcome {username}!")
            user_authenticated = True
        else:
            st.sidebar.warning("Free trial expired. Awaiting admin approval.")

# Admin panel
if is_admin:
    st.sidebar.title("🛠️ Admin Panel")
    st.sidebar.write("## Pending Approvals")
    for user in st.session_state.users:
        if not st.session_state.users[user]['approved']:
            if st.sidebar.button(f"Approve {user}"):
                st.session_state.users[user]['approved'] = True
                st.sidebar.success(f"{user} approved!")

# Main app logic after login
if user_authenticated:
    st.title("📊 Financial Ratio & Cash Flow Calculator")
    st.markdown("Calculate key financial ratios and cash flows based on your input figures.")

    company = st.text_input("Company Name", "")

    # Financial data inputs
    revenue = st.number_input("Revenue", min_value=0.0, value=0.0)
    cost_of_goods_sold = st.number_input("Cost of Goods Sold", min_value=0.0, value=0.0)
    operating_profit = st.number_input("Operating Profit", min_value=0.0, value=0.0)
    net_income = st.number_input("Net Income", min_value=0.0, value=0.0)
    total_assets = st.number_input("Total Assets", min_value=0.0, value=0.0)
    total_liabilities = st.number_input("Total Liabilities", min_value=0.0, value=0.0)
    equity = st.number_input("Equity", min_value=0.0, value=0.0)
    number_of_shares = st.number_input("Number of Shares Outstanding", min_value=0.0, value=0.0)

    # Cash Flow data
    operating_cash_flow = st.number_input("Operating Cash Flow", min_value=0.0, value=0.0)
    investing_cash_flow = st.number_input("Investing Cash Flow", min_value=0.0, value=0.0)
    financing_cash_flow = st.number_input("Financing Cash Flow", min_value=0.0, value=0.0)

    # Bank-specific inputs
    st.subheader("📌 Additional Banking Inputs")
    total_loans = st.number_input("Total Loans", min_value=0.0, value=0.0)
    total_deposits = st.number_input("Total Deposits", min_value=0.0, value=0.0)
    high_quality_liquid_assets = st.number_input("High-Quality Liquid Assets", min_value=0.0, value=0.0)
    net_cash_outflows_30d = st.number_input("Net Cash Outflows (30 days)", min_value=0.0, value=0.0)
    available_stable_funding = st.number_input("Available Stable Funding", min_value=0.0, value=0.0)
    required_stable_funding = st.number_input("Required Stable Funding", min_value=0.0, value=0.0)

    if st.button("📈 Calculate Ratios"):
        gross_profit = revenue - cost_of_goods_sold
        ratios_data = []

        insights = {
            "Gross Profit Margin": ("Measures profitability after direct costs.", "Higher is better; ensures core profitability.", "Improve pricing or reduce production costs."),
            "Net Profit Margin": ("Shows net profitability after all expenses.", "Low margins indicate high overhead or costs.", "Control operating expenses and debts."),
            "Operating Profit Margin": ("Reflects operational efficiency.", "Higher is preferred; operationally sound.", "Streamline operations and cut unnecessary costs."),
            "Return on Assets (ROA)": ("Measures asset efficiency in generating profit.", "Higher ratio signifies efficient asset use.", "Dispose underperforming assets, reinvest wisely."),
            "Return on Equity (ROE)": ("Shows return on shareholders' investment.", "High ROE implies good capital utilization.", "Increase retained earnings and effective leverage."),
            "Debt to Equity Ratio": ("Measures financial leverage.", "Too high indicates potential risk.", "Maintain optimal debt levels."),
            "Earnings per Share (EPS)": ("Indicates profitability per share.", "Higher EPS attracts investors.", "Boost net income or reduce shares."),
            "Loan-to-Deposit Ratio (LDR)": ("Measures liquidity and lending aggressiveness.", "Over 100% risky, under 80% too conservative.", "Balance between loans and deposits."),
            "Liquidity Coverage Ratio (LCR)": ("Ensures short-term liquidity.", "Under 100% signals risk.", "Maintain adequate high-quality assets."),
            "Net Stable Funding Ratio (NSFR)": ("Assesses medium-term stability.", "Below 100% is weak.", "Boost stable funding sources."),
        }

        if revenue:
            value = (gross_profit / revenue) * 100
            a, i, ad = insights["Gross Profit Margin"]
            ratios_data.append(["Gross Profit Margin", f"{value:.2f}%", a, i, ad])

        if total_deposits:
            value = (total_loans / total_deposits) * 100
            a, i, ad = insights["Loan-to-Deposit Ratio (LDR)"]
            ratios_data.append(["Loan-to-Deposit Ratio (LDR)", f"{value:.2f}%", a, i, ad])

        # Add similar blocks for the rest as needed using insights dict

        df = pd.DataFrame(ratios_data, columns=["Ratio", "Value", "Analysis", "Implication", "Advice"])
        st.dataframe(df)

        # CSV download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Download Results as CSV", data=csv, file_name=f'{company}_financial_ratios.csv', mime='text/csv')

else:
    st.warning("Please log in to access the financial calculator.")
