#Current Script

import streamlit as st
import pandas as pd

# Title and description
st.title("📊 Financial & Banking Ratios Dashboard")
st.markdown("Enter your financial data below and view key financial and banking-specific ratios.")

# Company and financial data
company = st.text_input("Company Name")

st.subheader("📑 General Financial Data")
revenue = st.number_input("Revenue", 0.0)
cost_of_goods_sold = st.number_input("Cost of Goods Sold", 0.0)
operating_profit = st.number_input("Operating Profit", 0.0)
net_income = st.number_input("Net Income", 0.0)
total_assets = st.number_input("Total Assets", 0.0)
total_liabilities = st.number_input("Total Liabilities", 0.0)
equity = st.number_input("Equity", 0.0)
number_of_shares = st.number_input("Number of Shares", 0.0)

st.subheader("💵 Cash Flows")
operating_cash_flow = st.number_input("Operating Cash Flow", 0.0)
investing_cash_flow = st.number_input("Investing Cash Flow", 0.0)
financing_cash_flow = st.number_input("Financing Cash Flow", 0.0)

st.subheader("🏦 Banking-Specific Data")
total_loans = st.number_input("Total Loans", 0.0)
total_deposits = st.number_input("Total Deposits", 0.0)
high_quality_liquid_assets = st.number_input("High-Quality Liquid Assets", 0.0)
net_cash_outflows_30d = st.number_input("Net Cash Outflows (30 Days)", 0.0)
available_stable_funding = st.number_input("Available Stable Funding", 0.0)
required_stable_funding = st.number_input("Required Stable Funding", 0.0)
non_performing_loans = st.number_input("Non-Performing Loans", 0.0)
loan_loss_reserves = st.number_input("Loan Loss Reserves", 0.0)
average_earning_assets = st.number_input("Average Earning Assets", 0.0)
operating_income = st.number_input("Operating Income", 0.0)
staff_costs = st.number_input("Staff Costs", 0.0)
tier_1_capital = st.number_input("Tier 1 Capital", 0.0)
tier_2_capital = st.number_input("Tier 2 Capital", 0.0)
risk_weighted_assets = st.number_input("Risk-Weighted Assets", 0.0)
net_open_position = st.number_input("Net Open Position (FX)", 0.0)
capital_base = st.number_input("Capital Base", 0.0)
dividends = st.number_input("Dividends Paid", 0.0)
deposit_growth = st.number_input("Deposit Growth (%)", 0.0)
loan_growth = st.number_input("Loan Growth (%)", 0.0)
book_value_per_share = st.number_input("Book Value Per Share", 0.0)

# Button to compute ratios
if st.button("📈 Calculate All Ratios"):
    gross_profit = revenue - cost_of_goods_sold

    ratios = []

    # Profitability Ratios
    if revenue:
        ratios.append({"Ratio": "Gross Profit Margin", "Value": f"{(gross_profit / revenue) * 100:.2f}%"})
        ratios.append({"Ratio": "Net Profit Margin", "Value": f"{(net_income / revenue) * 100:.2f}%"})
        ratios.append({"Ratio": "Operating Profit Margin", "Value": f"{(operating_profit / revenue) * 100:.2f}%"})

    if total_assets:
        ratios.append({"Ratio": "Return on Assets (ROA)", "Value": f"{(net_income / total_assets) * 100:.2f}%"})
    if equity:
        ratios.append({"Ratio": "Return on Equity (ROE)", "Value": f"{(net_income / equity) * 100:.2f}%"})
        ratios.append({"Ratio": "Debt-to-Equity Ratio", "Value": f"{(total_liabilities / equity):.2f}"})
    if number_of_shares:
        ratios.append({"Ratio": "Earnings Per Share (EPS)", "Value": f"{(net_income / number_of_shares):.2f}"})

    # Liquidity Ratios
    if total_deposits:
        ratios.append({"Ratio": "Loan-to-Deposit Ratio (LDR)", "Value": f"{(total_loans / total_deposits) * 100:.2f}%"})
    if net_cash_outflows_30d:
        ratios.append({"Ratio": "Liquidity Coverage Ratio (LCR)", "Value": f"{(high_quality_liquid_assets / net_cash_outflows_30d) * 100:.2f}%"})
    if required_stable_funding:
        ratios.append({"Ratio": "Net Stable Funding Ratio (NSFR)", "Value": f"{(available_stable_funding / required_stable_funding) * 100:.2f}%"})

    # Asset Quality Ratios
    if total_loans:
        ratios.append({"Ratio": "Non-Performing Loan Ratio (NPL)", "Value": f"{(non_performing_loans / total_loans) * 100:.2f}%"})
        ratios.append({"Ratio": "Loan Loss Reserve Ratio (LLR)", "Value": f"{(loan_loss_reserves / total_loans) * 100:.2f}%"})

    # Efficiency Ratios
    if average_earning_assets:
        ratios.append({"Ratio": "Net Interest Margin (NIM)", "Value": f"{(operating_income / average_earning_assets) * 100:.2f}%"})
    if operating_income:
        ratios.append({"Ratio": "Cost-to-Income Ratio (CIR)", "Value": f"{(staff_costs / operating_income) * 100:.2f}%"})

    # Capital Adequacy Ratios
    if risk_weighted_assets:
        ratios.append({"Ratio": "Capital Adequacy Ratio (CAR)", "Value": f"{(capital_base / risk_weighted_assets) * 100:.2f}%"})
        ratios.append({"Ratio": "Tier 1 Capital Ratio", "Value": f"{(tier_1_capital / risk_weighted_assets) * 100:.2f}%"})

    # FX Exposure
    if capital_base:
        ratios.append({"Ratio": "FX Net Open Position Limit", "Value": f"{(net_open_position / capital_base) * 100:.2f}%"})

    # Dividend Payout
    if net_income:
        ratios.append({"Ratio": "Dividend Payout Ratio", "Value": f"{(dividends / net_income) * 100:.2f}%"})

    # Growth Rates (as entered)
    ratios.append({"Ratio": "Deposit Growth Rate", "Value": f"{deposit_growth:.2f}%"})
    ratios.append({"Ratio": "Loan Growth Rate", "Value": f"{loan_growth:.2f}%"})

    # Valuation Metric
    if book_value_per_share:
        ratios.append({"Ratio": "Price-to-Book (P/B) Ratio", "Value": f"{(net_income / book_value_per_share):.2f}"})

    # Cash Flows
    ratios.append({"Ratio": "Operating Cash Flow", "Value": f"{operating_cash_flow:.2f}"})
    ratios.append({"Ratio": "Investing Cash Flow", "Value": f"{investing_cash_flow:.2f}"})
    ratios.append({"Ratio": "Financing Cash Flow", "Value": f"{financing_cash_flow:.2f}"})

    # Display results
    df_ratios = pd.DataFrame(ratios)
    st.subheader(f"📄 Ratios for {company}")
    st.dataframe(df_ratios)

    # Download to Excel
    excel_buffer = pd.ExcelWriter("ratios.xlsx", engine='xlsxwriter')
    df_ratios.to_excel(excel_buffer, index=False, sheet_name="Ratios")
    excel_buffer.close()

    with open("ratios.xlsx", "rb") as f:
        st.download_button("⬇️ Download Ratios as Excel", f, file_name=f"{company}_ratios.xlsx")

