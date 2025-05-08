import streamlit as st
import pandas as pd

# App title and sidebar navigation
st.set_page_config(page_title="📊 Financial Ratio Analyzer", layout="wide")
st.title("📊 Financial Ratio & Cash Flow Analyzer for Banks & Financial Institutions")

menu = ["Home", "Admin"]
choice = st.sidebar.selectbox("Navigation", menu)

# Dummy user authentication (can be replaced with real logic)
users = {"admin": "password123", "user": "userpass"}
# Admin page

if choice == "Admin":
    st.subheader("👨‍💼 Admin Panel")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in users and users[username] == password:
            st.success(f"Welcome, {username}!")
            st.write("Here you can manage the app settings or view logs.")
        else:
            st.error("Invalid credentials.")

# Home page
else:
    st.subheader("🏦 Enter Financial Data")

    company = st.text_input("Company Name")

    # Financial inputs
    revenue = st.number_input("Revenue", value=0.0)
    cost_of_goods_sold = st.number_input("Cost of Goods Sold", value=0.0)
    net_income = st.number_input("Net Income", value=0.0)
    operating_profit = st.number_input("Operating Profit", value=0.0)
    total_assets = st.number_input("Total Assets", value=0.0)
    equity = st.number_input("Equity", value=0.0)
    total_liabilities = st.number_input("Total Liabilities", value=0.0)
    number_of_shares = st.number_input("Number of Shares", value=0.0)

    # Cash Flows
    operating_cash_flow = st.number_input("Operating Cash Flow", value=0.0)
    investing_cash_flow = st.number_input("Investing Cash Flow", value=0.0)
    financing_cash_flow = st.number_input("Financing Cash Flow", value=0.0)

    # Banking Specific
    total_deposits = st.number_input("Total Deposits", value=0.0)
    total_loans = st.number_input("Total Loans", value=0.0)
    high_quality_liquid_assets = st.number_input("High-Quality Liquid Assets", value=0.0)
    net_cash_outflows_30d = st.number_input("Net Cash Outflows (30 days)", value=0.0)
    available_stable_funding = st.number_input("Available Stable Funding", value=0.0)
    required_stable_funding = st.number_input("Required Stable Funding", value=0.0)
    non_performing_loans = st.number_input("Non-Performing Loans", value=0.0)
    net_interest_income = st.number_input("Net Interest Income", value=0.0)
    average_earning_assets = st.number_input("Average Earning Assets", value=0.0)
    operating_income = st.number_input("Operating Income", value=0.0)
    staff_costs = st.number_input("Staff Costs", value=0.0)
    risk_weighted_assets = st.number_input("Risk Weighted Assets", value=0.0)
    tier1_capital = st.number_input("Tier 1 Capital", value=0.0)
    tier2_capital = st.number_input("Tier 2 Capital", value=0.0)
    total_assets_bank = st.number_input("Total Bank Assets", value=0.0)
    net_open_position = st.number_input("Net Open Position", value=0.0)
    capital_base = st.number_input("Capital Base", value=0.0)
    book_value = st.number_input("Book Value", value=0.0)

    # Button to calculate ratios and save results
    if st.button("📈 Calculate Ratios & Cash Flows"):
        gross_profit = revenue - cost_of_goods_sold
        ratios_data = []

        # Cash Flows
        ratios_data.append({"Ratio": "Operating Cash Flow", "Value": f"{operating_cash_flow:.2f}"})
        ratios_data.append({"Ratio": "Investing Cash Flow", "Value": f"{investing_cash_flow:.2f}"})
        ratios_data.append({"Ratio": "Financing Cash Flow", "Value": f"{financing_cash_flow:.2f}"})

        # Profitability Ratios
        if revenue:
            ratios_data.append({"Ratio": "Gross Profit Margin", "Value": f"{(gross_profit / revenue) * 100:.2f}%"})
            ratios_data.append({"Ratio": "Net Profit Margin", "Value": f"{(net_income / revenue) * 100:.2f}%"})
            ratios_data.append({"Ratio": "Operating Profit Margin", "Value": f"{(operating_profit / revenue) * 100:.2f}%"})

        if total_assets:
            ratios_data.append({"Ratio": "Return on Assets (ROA)", "Value": f"{(net_income / total_assets) * 100:.2f}%"})

        if equity:
            ratios_data.append({"Ratio": "Return on Equity (ROE)", "Value": f"{(net_income / equity) * 100:.2f}%"})
            ratios_data.append({"Ratio": "Debt to Equity Ratio", "Value": f"{(total_liabilities / equity):.2f}"})

        if number_of_shares:
            ratios_data.append({"Ratio": "Earnings per Share (EPS)", "Value": f"{(net_income / number_of_shares):.2f}"})

        # Banking Ratios
        if total_deposits:
            ratios_data.append({"Ratio": "Loan-to-Deposit Ratio (LDR)", "Value": f"{(total_loans / total_deposits) * 100:.2f}%"})

        if net_cash_outflows_30d:
            ratios_data.append({"Ratio": "Liquidity Coverage Ratio (LCR)", "Value": f"{(high_quality_liquid_assets / net_cash_outflows_30d) * 100:.2f}%"})

        if required_stable_funding:
            ratios_data.append({"Ratio": "Net Stable Funding Ratio (NSFR)", "Value": f"{(available_stable_funding / required_stable_funding) * 100:.2f}%"})

        if total_loans:
            ratios_data.append({"Ratio": "Non-Performing Loan (NPL) Ratio", "Value": f"{(non_performing_loans / total_loans) * 100:.2f}%"})

        if average_earning_assets:
            ratios_data.append({"Ratio": "Net Interest Margin (NIM)", "Value": f"{(net_interest_income / average_earning_assets) * 100:.2f}%"})

        if operating_income:
            ratios_data.append({"Ratio": "Cost to Income Ratio", "Value": f"{(staff_costs / operating_income) * 100:.2f}%"})

        if risk_weighted_assets:
            ratios_data.append({"Ratio": "Capital Adequacy Ratio (CAR)", "Value": f"{((tier1_capital + tier2_capital) / risk_weighted_assets) * 100:.2f}%"})

        if total_assets_bank:
            ratios_data.append({"Ratio": "Leverage Ratio", "Value": f"{(tier1_capital / total_assets_bank) * 100:.2f}%"})

        if capital_base:
            ratios_data.append({"Ratio": "Foreign Exchange Exposure Ratio", "Value": f"{(net_open_position / capital_base) * 100:.2f}%"})

        if number_of_shares:
            ratios_data.append({"Ratio": "Book Value per Share", "Value": f"{(book_value / number_of_shares):.2f}"})

        # Add empty columns for Analysis, Implication, Advice
        for row in ratios_data:
            row["Analysis"] = ""
            row["Implication"] = ""
            row["Advice"] = ""

        # Display result DataFrame
        df = pd.DataFrame(ratios_data)
        st.dataframe(df)

        # Download CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv,
            file_name=f"{company}_financial_ratios.csv",
            mime='text/csv'
        )
