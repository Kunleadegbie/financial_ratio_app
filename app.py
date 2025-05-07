# New Revised script
# (Your app.py code from previous message here. 
# For brevity, I'm keeping it summarized in this comment — it will be included in the actual file.)

import streamlit as st
import pandas as pd
from io import BytesIO
import os

# File to store user accounts
USERS_CSV = "users.csv"

# Load or create the user database
if os.path.exists(USERS_CSV):
    df_users = pd.read_csv(USERS_CSV)
else:
    df_users = pd.DataFrame(columns=["username", "password", "role"])

# User authentication
st.sidebar.title("🔐 Login")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
role = None

if st.sidebar.button("Login"):
    user_record = df_users[(df_users["username"] == username) & (df_users["password"] == password)]
    if not user_record.empty:
        st.sidebar.success(f"Welcome {username}!")
        role = user_record.iloc[0]["role"]
    else:
        st.sidebar.error("Invalid username or password.")

# Admin Registration
if st.sidebar.checkbox("Create Admin Account"):
    new_admin_username = st.sidebar.text_input("New Admin Username")
    new_admin_password = st.sidebar.text_input("New Admin Password", type="password")
    if st.sidebar.button("Register Admin"):
        if new_admin_username and new_admin_password:
            new_admin = pd.DataFrame([{"username": new_admin_username, "password": new_admin_password, "role": "admin"}])
            df_users = pd.concat([df_users, new_admin], ignore_index=True)
            df_users.to_csv(USERS_CSV, index=False)
            st.sidebar.success("New admin registered successfully.")
        else:
            st.sidebar.error("Please provide both username and password.")

# Main dashboard
if role:
    st.title("📊 Financial Ratio & Cash Flow Calculator")

    company = st.text_input("Company Name", "")

    st.header("General Financial Data")
    revenue = st.number_input("Revenue", min_value=0.0, value=0.0)
    cost_of_goods_sold = st.number_input("Cost of Goods Sold", min_value=0.0, value=0.0)
    operating_profit = st.number_input("Operating Profit", min_value=0.0, value=0.0)
    net_income = st.number_input("Net Income", min_value=0.0, value=0.0)
    total_assets = st.number_input("Total Assets", min_value=0.0, value=0.0)
    total_liabilities = st.number_input("Total Liabilities", min_value=0.0, value=0.0)
    equity = st.number_input("Equity", min_value=0.0, value=0.0)
    number_of_shares = st.number_input("Number of Shares Outstanding", min_value=0.0, value=0.0)

    st.header("Cash Flow Data")
    operating_cash_flow = st.number_input("Operating Cash Flow", min_value=0.0, value=0.0)
    investing_cash_flow = st.number_input("Investing Cash Flow", min_value=0.0, value=0.0)
    financing_cash_flow = st.number_input("Financing Cash Flow", min_value=0.0, value=0.0)

    st.header("Banking Financial Data")
    total_loans = st.number_input("Total Loans", min_value=0.0, value=0.0)
    total_deposits = st.number_input("Total Deposits", min_value=0.0, value=0.0)
    non_performing_loans = st.number_input("Non-Performing Loans", min_value=0.0, value=0.0)

    if st.button("📈 Calculate Ratios & Cash Flows"):
        gross_profit = revenue - cost_of_goods_sold
        ratios_data = []

        # Profitability Ratios
        if revenue != 0:
            ratios_data.append({"Ratio": "Gross Profit Margin", "Value": f"{(gross_profit / revenue) * 100:.2f}%",
                                "Analysis": "Higher is better", "Implication": "Shows profitability after production costs",
                                "Advice": "Increase gross margin by cutting costs or raising revenue"})
            ratios_data.append({"Ratio": "Net Profit Margin", "Value": f"{(net_income / revenue) * 100:.2f}%",
                                "Analysis": "Higher is better", "Implication": "Measures bottom-line profitability",
                                "Advice": "Control costs and boost revenue"})
            ratios_data.append({"Ratio": "Operating Profit Margin", "Value": f"{(operating_profit / revenue) * 100:.2f}%",
                                "Analysis": "Higher is better", "Implication": "Efficiency of core operations",
                                "Advice": "Streamline operational costs"})

        if total_assets != 0:
            ratios_data.append({"Ratio": "Return on Assets (ROA)", "Value": f"{(net_income / total_assets) * 100:.2f}%",
                                "Analysis": "Higher is better", "Implication": "Asset profitability",
                                "Advice": "Utilize assets more efficiently"})

        if equity != 0:
            ratios_data.append({"Ratio": "Return on Equity (ROE)", "Value": f"{(net_income / equity) * 100:.2f}%",
                                "Analysis": "Higher is better", "Implication": "Shareholder profitability",
                                "Advice": "Improve profit margins or asset efficiency"})
            ratios_data.append({"Ratio": "Debt to Equity Ratio", "Value": f"{(total_liabilities / equity):.2f}",
                                "Analysis": "Lower is safer", "Implication": "Financial leverage risk",
                                "Advice": "Reduce debts or increase equity"})

        if number_of_shares != 0:
            ratios_data.append({"Ratio": "Earnings per Share (EPS)", "Value": f"{(net_income / number_of_shares):.2f}",
                                "Analysis": "Higher is better", "Implication": "Shareholder value",
                                "Advice": "Boost net income or repurchase shares"})

        # Cash Flow Ratios
        ratios_data.append({"Ratio": "Operating Cash Flow", "Value": f"{operating_cash_flow:,.2f}",
                            "Analysis": "Higher is healthier", "Implication": "Operating liquidity",
                            "Advice": "Improve operational cash generation"})
        ratios_data.append({"Ratio": "Investing Cash Flow", "Value": f"{investing_cash_flow:,.2f}",
                            "Analysis": "Negative if investing", "Implication": "Capex/Investment activities",
                            "Advice": "Monitor investment spending"})
        ratios_data.append({"Ratio": "Financing Cash Flow", "Value": f"{financing_cash_flow:,.2f}",
                            "Analysis": "Depends on strategy", "Implication": "Debt/Equity financing",
                            "Advice": "Balance financing methods"})

        # Banking Ratios
        ratios_data.append({"Ratio": "Loan-to-Deposit Ratio (LDR)", "Value": f"{(total_loans / total_deposits):.2%}" if total_deposits else "N/A",
                            "Analysis": "Optimal between 80%-90%", "Implication": "Liquidity risk if too high",
                            "Advice": "Balance lending and deposits"})
        ratios_data.append({"Ratio": "Non-Performing Loan (NPL) Ratio", "Value": f"{(non_performing_loans / total_loans):.2%}" if total_loans else "N/A",
                            "Analysis": "Lower is better", "Implication": "Credit risk exposure",
                            "Advice": "Tighten credit risk management"})

        # Convert to DataFrame and display
        ratios_df = pd.DataFrame(ratios_data)
        st.subheader(f"📊 Financial Ratios for {company if company else 'the Company'}")
        st.dataframe(ratios_df)

        # CSV Download
        csv_buffer = BytesIO()
        ratios_df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)

        st.download_button(
            label="📥 Download Ratios as CSV",
            data=csv_buffer,
            file_name=f"{company.replace(' ', '_')}_financial_ratios.csv" if company else "financial_ratios.csv",
            mime="text/csv"
        )
else:
    st.warning("Please log in to access the financial dashboard.")
