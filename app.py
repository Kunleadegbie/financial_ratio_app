# New script
# (Your app.py code from previous message here. 
# For brevity, I'm keeping it summarized in this comment — it will be included in the actual file.)

import streamlit as st
import pandas as pd
from io import BytesIO
import os

# Constants
USERS_CSV = "users.csv"

# Ensure users.csv exists
if not os.path.exists(USERS_CSV):
    df = pd.DataFrame(columns=["username", "role"])
    df.to_csv(USERS_CSV, index=False)

# App Title
st.title("📊 Financial Ratio & Cash Flow Calculator (Extended Edition)")

# User login simulation
username = st.text_input("Enter your username to proceed:")
role = st.selectbox("Select your role:", ["Admin", "User"])

# Save new user info if not already saved
users_df = pd.read_csv(USERS_CSV)
if username and username not in users_df["username"].values:
    new_entry = pd.DataFrame({"username": [username], "role": [role]})
    users_df = pd.concat([users_df, new_entry], ignore_index=True)
    users_df.to_csv(USERS_CSV, index=False)

# Company input
company = st.text_input("Company Name", "")

# Financial data inputs
st.header("General Financial Data")
revenue = st.number_input("Revenue", min_value=0.0, value=0.0)
cost_of_goods_sold = st.number_input("Cost of Goods Sold", min_value=0.0, value=0.0)
operating_profit = st.number_input("Operating Profit", min_value=0.0, value=0.0)
net_income = st.number_input("Net Income", min_value=0.0, value=0.0)
total_assets = st.number_input("Total Assets", min_value=0.0, value=0.0)
total_liabilities = st.number_input("Total Liabilities", min_value=0.0, value=0.0)
equity = st.number_input("Equity", min_value=0.0, value=0.0)
number_of_shares = st.number_input("Number of Shares Outstanding", min_value=0.0, value=0.0)

# Cash Flow data
st.header("Cash Flow Data")
operating_cash_flow = st.number_input("Operating Cash Flow", min_value=0.0, value=0.0)
investing_cash_flow = st.number_input("Investing Cash Flow", min_value=0.0, value=0.0)
financing_cash_flow = st.number_input("Financing Cash Flow", min_value=0.0, value=0.0)

# Banking-specific financial data
st.header("Banking Financial Data")
total_loans = st.number_input("Total Loans", min_value=0.0, value=0.0)
total_deposits = st.number_input("Total Deposits", min_value=0.0, value=0.0)
non_performing_loans = st.number_input("Non-Performing Loans", min_value=0.0, value=0.0)

# Calculate button
if st.button("📈 Calculate Ratios & Analysis"):
    gross_profit = revenue - cost_of_goods_sold
    ratios_data = []

    # Cash Flows
    net_cash_flow = operating_cash_flow + investing_cash_flow + financing_cash_flow
    ratios_data.append({"Ratio": "Net Cash Flow", "Value": net_cash_flow, "Analysis": "Positive" if net_cash_flow >= 0 else "Negative",
                        "Implication": "Healthy cash flow" if net_cash_flow >= 0 else "Negative cash movement",
                        "Advice": "Maintain positive cash flow." if net_cash_flow >= 0 else "Improve cash-generating activities."})

    # Profitability Ratios
    if revenue != 0:
        ratios_data.append({"Ratio": "Gross Profit Margin", "Value": f"{(gross_profit / revenue) * 100:.2f}%", "Analysis": "",
                            "Implication": "", "Advice": ""})
        ratios_data.append({"Ratio": "Net Profit Margin", "Value": f"{(net_income / revenue) * 100:.2f}%", "Analysis": "",
                            "Implication": "", "Advice": ""})
        ratios_data.append({"Ratio": "Operating Profit Margin", "Value": f"{(operating_profit / revenue) * 100:.2f}%", "Analysis": "",
                            "Implication": "", "Advice": ""})

    if total_assets != 0:
        ratios_data.append({"Ratio": "Return on Assets (ROA)", "Value": f"{(net_income / total_assets) * 100:.2f}%", "Analysis": "",
                            "Implication": "", "Advice": ""})

    if equity != 0:
        ratios_data.append({"Ratio": "Return on Equity (ROE)", "Value": f"{(net_income / equity) * 100:.2f}%", "Analysis": "",
                            "Implication": "", "Advice": ""})
        ratios_data.append({"Ratio": "Debt to Equity Ratio", "Value": f"{(total_liabilities / equity):.2f}", "Analysis": "",
                            "Implication": "", "Advice": ""})

    if number_of_shares != 0:
        ratios_data.append({"Ratio": "Earnings per Share (EPS)", "Value": f"{(net_income / number_of_shares):.2f}", "Analysis": "",
                            "Implication": "", "Advice": ""})

    # Banking Ratios
    ldr = total_loans / total_deposits if total_deposits != 0 else 0.0
    ratios_data.append({"Ratio": "Loan-to-Deposit Ratio (LDR)", "Value": f"{ldr:.2%}", "Analysis": "",
                        "Implication": "", "Advice": ""})

    npl_ratio = non_performing_loans / total_loans if total_loans != 0 else 0.0
    ratios_data.append({"Ratio": "Non-Performing Loan (NPL) Ratio", "Value": f"{npl_ratio:.2%}", "Analysis": "",
                        "Implication": "", "Advice": ""})

    # Convert to DataFrame
    ratios_df = pd.DataFrame(ratios_data)

    # Display results
    st.subheader(f"📊 Financial Ratios and Analysis for {company if company else 'the Company'}")
    st.dataframe(ratios_df)

    # CSV Download
    csv_buffer = BytesIO()
    ratios_df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    st.download_button(
        label="📥 Download Report as CSV",
        data=csv_buffer,
        file_name=f"{company.replace(' ', '_')}_financial_analysis.csv" if company else "financial_analysis.csv",
        mime="text/csv"
    )

# Display users list for Admin only
if role == "Admin":
    st.sidebar.subheader("👥 Registered Users (Admin View)")
    st.sidebar.dataframe(users_df)

