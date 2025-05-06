import streamlit as st
import pandas as pd
from io import BytesIO

# App title and header
st.title("📊 Financial Ratio & Cash Flow Calculator")
st.markdown("Calculate key financial and banking sector ratios based on your input figures.")

# User inputs
company = st.text_input("Company Name", "")

# --- Financial data inputs ---
st.subheader("📌 General Financial Data")
revenue = st.number_input("Revenue", min_value=0.0, value=0.0)
cost_of_goods_sold = st.number_input("Cost of Goods Sold", min_value=0.0, value=0.0)
operating_profit = st.number_input("Operating Profit", min_value=0.0, value=0.0)
net_income = st.number_input("Net Income", min_value=0.0, value=0.0)
total_assets = st.number_input("Total Assets", min_value=0.0, value=0.0)
total_liabilities = st.number_input("Total Liabilities", min_value=0.0, value=0.0)
equity = st.number_input("Equity", min_value=0.0, value=0.0)
number_of_shares = st.number_input("Number of Shares Outstanding", min_value=0.0, value=0.0)

# Cash Flow data
st.subheader("📌 Cash Flow Data")
operating_cash_flow = st.number_input("Operating Cash Flow", min_value=0.0, value=0.0)
investing_cash_flow = st.number_input("Investing Cash Flow", min_value=0.0, value=0.0)
financing_cash_flow = st.number_input("Financing Cash Flow", min_value=0.0, value=0.0)

# --- Banking Specific Inputs ---
st.subheader("🏦 Liquidity Ratios (Banks)")
total_loans = st.number_input("Total Loans", min_value=0.0, value=0.0)
total_deposits = st.number_input("Total Deposits", min_value=0.0, value=0.0)
hql_assets = st.number_input("High-Quality Liquid Assets", min_value=0.0, value=0.0)
net_cash_outflows_30d = st.number_input("Total Net Cash Outflows (30 days)", min_value=0.0, value=0.0)
available_stable_funding = st.number_input("Available Stable Funding", min_value=0.0, value=0.0)
required_stable_funding = st.number_input("Required Stable Funding", min_value=0.0, value=0.0)

st.subheader("🏦 Asset Quality Ratios")
non_performing_loans = st.number_input("Non-Performing Loans", min_value=0.0, value=0.0)
loan_loss_reserves = st.number_input("Loan Loss Reserves", min_value=0.0, value=0.0)
gross_loans = st.number_input("Gross Loans", min_value=0.0, value=0.0)

st.subheader("🏦 Profitability & Efficiency Ratios (Banks)")
net_interest_income = st.number_input("Net Interest Income", min_value=0.0, value=0.0)
avg_earning_assets = st.number_input("Average Earning Assets", min_value=0.0, value=0.0)
operating_income = st.number_input("Operating Income", min_value=0.0, value=0.0)
staff_costs = st.number_input("Staff Costs", min_value=0.0, value=0.0)

st.subheader("🏦 Capital Adequacy Ratios (Basel)")
tier_1_capital = st.number_input("Tier 1 Capital", min_value=0.0, value=0.0)
tier_2_capital = st.number_input("Tier 2 Capital", min_value=0.0, value=0.0)
risk_weighted_assets = st.number_input("Risk-Weighted Assets", min_value=0.0, value=0.0)

st.subheader("📊 Market Risk Ratios")
net_open_position = st.number_input("Net Open FX Position", min_value=0.0, value=0.0)
capital_base = st.number_input("Capital Base", min_value=0.0, value=0.0)
# Value at Risk (VaR) - input for info
var_value = st.number_input("Value at Risk (VaR)", min_value=0.0, value=0.0)

st.subheader("📊 Growth & Dividend Ratios")
deposit_growth = st.number_input("Deposit Growth Amount", min_value=0.0, value=0.0)
loan_growth = st.number_input("Loan Growth Amount", min_value=0.0, value=0.0)
dividends_paid = st.number_input("Dividends Paid", min_value=0.0, value=0.0)
book_value = st.number_input("Book Value of Equity", min_value=0.0, value=0.0)

# Button to calculate ratios
if st.button("📈 Calculate Ratios & Cash Flows"):

    gross_profit = revenue - cost_of_goods_sold
    ratios_data = []

    # Cash Flows
    ratios_data += [
        {"Ratio": "Operating Cash Flow", "Value": f"{operating_cash_flow:.2f}"},
        {"Ratio": "Investing Cash Flow", "Value": f"{investing_cash_flow:.2f}"},
        {"Ratio": "Financing Cash Flow", "Value": f"{financing_cash_flow:.2f}"}
    ]

    # Profitability Ratios
    if revenue:
        ratios_data.append({"Ratio": "Gross Profit Margin", "Value": f"{(gross_profit/revenue)*100:.2f}%"})
        ratios_data.append({"Ratio": "Net Profit Margin", "Value": f"{(net_income/revenue)*100:.2f}%"})
        ratios_data.append({"Ratio": "Operating Profit Margin", "Value": f"{(operating_profit/revenue)*100:.2f}%"})

    if total_assets:
        ratios_data.append({"Ratio": "Return on Assets (ROA)", "Value": f"{(net_income/total_assets)*100:.2f}%"})
        ratios_data.append({"Ratio": "Asset Turnover", "Value": f"{(revenue/total_assets):.2f}"})

    if equity:
        ratios_data.append({"Ratio": "Return on Equity (ROE)", "Value": f"{(net_income/equity)*100:.2f}%"})
        ratios_data.append({"Ratio": "Debt to Equity Ratio", "Value": f"{(total_liabilities/equity):.2f}"})

    if number_of_shares:
        ratios_data.append({"Ratio": "Earnings per Share (EPS)", "Value": f"{(net_income/number_of_shares):.2f}"})
        if net_income:
            ratios_data.append({"Ratio": "Dividend Payout Ratio", "Value": f"{(dividends_paid/net_income)*100:.2f}%"})

    if book_value and number_of_shares:
        ratios_data.append({"Ratio": "Book Value per Share", "Value": f"{(book_value/number_of_shares):.2f}"})

    # Liquidity Ratios
    if total_deposits:
        ratios_data.append({"Ratio": "Loan-to-Deposit Ratio (LDR)", "Value": f"{(total_loans/total_deposits)*100:.2f}%"})
    if net_cash_outflows_30d:
        ratios_data.append({"Ratio": "Liquidity Coverage Ratio (LCR)", "Value": f"{(hql_assets/net_cash_outflows_30d)*100:.2f}%"})
    if required_stable_funding:
        ratios_data.append({"Ratio": "Net Stable Funding Ratio (NSFR)", "Value": f"{(available_stable_funding/required_stable_funding)*100:.2f}%"})

    # Asset Quality Ratios
    if total_loans:
        ratios_data.append({"Ratio": "Non-Performing Loan (NPL) Ratio", "Value": f"{(non_performing_loans/total_loans)*100:.2f}%"})
    if gross_loans:
        ratios_data.append({"Ratio": "Loan Loss Reserve to Gross Loans", "Value": f"{(loan_loss_reserves/gross_loans)*100:.2f}%"})
    if non_performing_loans:
        ratios_data.append({"Ratio": "Provision Coverage Ratio", "Value": f"{(loan_loss_reserves/non_performing_loans)*100:.2f}%"})

    # Profitability (Banks)
    if avg_earning_assets:
        ratios_data.append({"Ratio": "Net Interest Margin (NIM)", "Value": f"{(net_interest_income/avg_earning_assets)*100:.2f}%"})
    if operating_income:
        ratios_data.append({"Ratio": "Cost-to-Income Ratio", "Value": f"{(operating_profit/operating_income)*100:.2f}%"})
        ratios_data.append({"Ratio": "Staff Cost to Income Ratio", "Value": f"{(staff_costs/operating_income)*100:.2f}%"})

    # Capital Adequacy
    if risk_weighted_assets:
        ratios_data.append({"Ratio": "Capital Adequacy Ratio (CAR)", "Value": f"{((tier_1_capital + tier_2_capital)/risk_weighted_assets)*100:.2f}%"})
        ratios_data.append({"Ratio": "Tier 1 Capital Ratio", "Value": f"{(tier_1_capital/risk_weighted_assets)*100:.2f}%"})
    if total_assets:
        ratios_data.append({"Ratio": "Leverage Ratio", "Value": f"{(tier_1_capital/total_assets)*100:.2f}%"})

    # Market Risk
    if capital_base:
        ratios_data.append({"Ratio": "FX Exposure Ratio", "Value": f"{(net_open_position/capital_base)*100:.2f}%"})

    # Growth Ratios
    if total_deposits:
        ratios_data.append({"Ratio": "Deposit Growth Rate", "Value": f"{(deposit_growth/total_deposits)*100:.2f}%"})
    if total_loans:
        ratios_data.append({"Ratio": "Loan Growth Rate", "Value": f"{(loan_growth/total_loans)*100:.2f}%"})

    # Display results
    st.subheader(f"📊 Financial Ratios for {company if company else 'the Company'}")
    ratios_df = pd.DataFrame(ratios_data)
    st.dataframe(ratios_df)

    # Download button
    csv_buffer = BytesIO()
    ratios_df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    st.download_button(
        label="📥 Download Ratios as CSV",
        data=csv_buffer,
        file_name=f"{company.replace(' ', '_')}_financial_ratios.csv" if company else "financial_ratios.csv",
        mime="text/csv"
    )
