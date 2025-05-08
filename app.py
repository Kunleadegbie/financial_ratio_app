import streamlit as st
import pandas as pd
from io import BytesIO

# Simple Login
def login():
    st.title("🔒 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "chumcred" and password == "1234":
            st.session_state.logged_in = True
        else:
            st.error("Invalid username or password")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
else:
    # App title and header
    st.title("📊 Financial Ratio & Cash Flow Calculator")
    st.markdown("Calculate key financial ratios and cash flows based on your input figures.")

    # User inputs
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
    cash_and_equivalents = st.number_input("Cash and Cash Equivalents", min_value=0.0, value=0.0)
    current_assets = st.number_input("Current Assets", min_value=0.0, value=0.0)
    current_liabilities = st.number_input("Current Liabilities", min_value=0.0, value=0.0)
    inventory = st.number_input("Inventory", min_value=0.0, value=0.0)

    if st.button("📈 Calculate Ratios & Cash Flows"):
        gross_profit = revenue - cost_of_goods_sold
        ratios_data = []

        # Cash Flows
        ratios_data.append({"Ratio": "Operating Cash Flow", "Value": f"{operating_cash_flow:.2f}", "Analysis": "", "Implication": "", "Advice": ""})
        ratios_data.append({"Ratio": "Investing Cash Flow", "Value": f"{investing_cash_flow:.2f}", "Analysis": "", "Implication": "", "Advice": ""})
        ratios_data.append({"Ratio": "Financing Cash Flow", "Value": f"{financing_cash_flow:.2f}", "Analysis": "", "Implication": "", "Advice": ""})

        # Profitability Ratios
        if revenue:
            ratios_data.append({"Ratio": "Gross Profit Margin", "Value": f"{(gross_profit / revenue) * 100:.2f}%", "Analysis": "", "Implication": "", "Advice": ""})
            ratios_data.append({"Ratio": "Net Profit Margin", "Value": f"{(net_income / revenue) * 100:.2f}%", "Analysis": "", "Implication": "", "Advice": ""})
            ratios_data.append({"Ratio": "Operating Profit Margin", "Value": f"{(operating_profit / revenue) * 100:.2f}%", "Analysis": "", "Implication": "", "Advice": ""})

        if total_assets:
            ratios_data.append({"Ratio": "Return on Assets (ROA)", "Value": f"{(net_income / total_assets) * 100:.2f}%", "Analysis": "", "Implication": "", "Advice": ""})

        if equity:
            ratios_data.append({"Ratio": "Return on Equity (ROE)", "Value": f"{(net_income / equity) * 100:.2f}%", "Analysis": "", "Implication": "", "Advice": ""})
            ratios_data.append({"Ratio": "Debt to Equity Ratio", "Value": f"{(total_liabilities / equity):.2f}", "Analysis": "", "Implication": "", "Advice": ""})

        if number_of_shares:
            ratios_data.append({"Ratio": "Earnings per Share (EPS)", "Value": f"{(net_income / number_of_shares):.2f}", "Analysis": "", "Implication": "", "Advice": ""})

        # Liquidity Ratios
        if current_liabilities:
            ratios_data.append({"Ratio": "Current Ratio", "Value": f"{(current_assets / current_liabilities):.2f}", "Analysis": "", "Implication": "", "Advice": ""})
            ratios_data.append({"Ratio": "Quick Ratio", "Value": f"{((current_assets - inventory) / current_liabilities):.2f}", "Analysis": "", "Implication": "", "Advice": ""})
            ratios_data.append({"Ratio": "Cash Ratio", "Value": f"{(cash_and_equivalents / current_liabilities):.2f}", "Analysis": "", "Implication": "", "Advice": ""})

        net_cash_flow = operating_cash_flow + investing_cash_flow + financing_cash_flow
        ratios_data.append({"Ratio": "Net Cash Flow", "Value": f"{net_cash_flow:.2f}", "Analysis": "", "Implication": "", "Advice": ""})

        # Display result
        st.subheader("📊 Calculated Financial Ratios & Cash Flows")
        df = pd.DataFrame(ratios_data)
        st.dataframe(df)

        # Download to CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Ratios as CSV",
            data=csv,
            file_name=f"{company}_financial_ratios.csv",
            mime="text/csv"
        )
