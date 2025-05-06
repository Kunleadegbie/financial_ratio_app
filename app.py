#Updated Script

import streamlit as st
import pandas as pd
from io import BytesIO

# App title and header
st.title("📊 Financial Ratio & Cash Flow Calculator")
st.markdown("Calculate key financial ratios and cash flows based on your input figures.")

# User inputs
company = st.text_input("Company Name", "")

# Financial data inputs
st.subheader("📑 Financial Data")
revenue = st.number_input("Revenue", min_value=0.0, value=0.0)
cost_of_goods_sold = st.number_input("Cost of Goods Sold", min_value=0.0, value=0.0)
operating_profit = st.number_input("Operating Profit", min_value=0.0, value=0.0)
net_income = st.number_input("Net Income", min_value=0.0, value=0.0)
total_assets = st.number_input("Total Assets", min_value=0.0, value=0.0)
total_liabilities = st.number_input("Total Liabilities", min_value=0.0, value=0.0)
equity = st.number_input("Equity", min_value=0.0, value=0.0)
number_of_shares = st.number_input("Number of Shares Outstanding", min_value=0.0, value=0.0)

# Cash Flow data
st.subheader("💵 Cash Flow Data")
operating_cash_flow = st.number_input("Operating Cash Flow", min_value=0.0, value=0.0)
investing_cash_flow = st.number_input("Investing Cash Flow", min_value=0.0, value=0.0)
financing_cash_flow = st.number_input("Financing Cash Flow", min_value=0.0, value=0.0)

# Banking-specific inputs
st.subheader("🏦 Banking-Specific Inputs")
total_loans = st.number_input("Total Loans", min_value=0.0, value=0.0)
total_deposits = st.number_input("Total Deposits", min_value=0.0, value=0.0)
high_quality_liquid_assets = st.number_input("High-Quality Liquid Assets", min_value=0.0, value=0.0)
net_cash_outflows_30d = st.number_input("Net Cash Outflows (30 days)", min_value=0.0, value=0.0)
available_stable_funding = st.number_input("Available Stable Funding", min_value=0.0, value=0.0)
required_stable_funding = st.number_input("Required Stable Funding", min_value=0.0, value=0.0)
non_performing_loans = st.number_input("Non-Performing Loans", min_value=0.0, value=0.0)
loan_loss_reserves = st.number_input("Loan Loss Reserves", min_value=0.0, value=0.0)
average_earning_assets = st.number_input("Average Earning Assets", min_value=0.0, value=0.0)
operating_income = st.number_input("Operating Income", min_value=0.0, value=0.0)
staff_costs = st.number_input("Staff Costs", min_value=0.0, value=0.0)
tier_1_capital = st.number_input("Tier 1 Capital", min_value=0.0, value=0.0)
tier_2_capital = st.number_input("Tier 2 Capital", min_value=0.0, value=0.0)
risk_weighted_assets = st.number_input("Risk-Weighted Assets", min_value=0.0, value=0.0)
net_open_position = st.number_input("Net Open Position (FX)", min_value=0.0, value=0.0)
capital_base = st.number_input("Capital Base", min_value=0.0, value=0.0)
dividends = st.number_input("Dividends Paid", min_value=0.0, value=0.0)
deposit_growth = st.number_input("Deposit Growth Rate (%)", min_value=0.0, value=0.0)
loan_growth = st.number_input("Loan Growth Rate (%)", min_value=0.0, value=0.0)
book_value_per_share = st.number_input("Book Value per Share", min_value=0.0, value=0.0)

# Button to calculate ratios
if st.button("📈 Calculate Ratios & Cash Flows"):
    gross_profit = revenue - cost_of_goods_sold
    ratios_data = []

    # Cash Flows
    ratios_data.extend([
        {"Ratio": "Operating Cash Flow", "Value": f"{operating_cash_flow:.2f}"},
        {"Ratio": "Investing Cash Flow", "Value": f"{investing_cash_flow:.2f}"},
        {"Ratio": "Financing Cash Flow", "Value": f"{financing_cash_flow:.2f}"}
    ])

    # Profitability Ratios
    if revenue != 0:
        ratios_data.extend([
            {"Ratio": "Gross Profit Margin", "Value": f"{(gross_profit / revenue) * 100:.2f}%"},
            {"Ratio": "Net Profit Margin", "Value": f"{(net_income / revenue) * 100:.2f}%"},
            {"Ratio": "Operating Profit Margin", "Value": f"{(operating_profit / revenue) * 100:.2f}%"}
        ])
    if total_assets != 0:
        ratios_data.append({"Ratio": "Return on Assets (ROA)", "Value": f"{(net_income / total_assets) * 100:.2f}%"})
    if equity != 0:
        ratios_data.append({"Ratio": "Return on Equity (ROE)", "Value": f"{(net_income / equity) * 100:.2f}%"})
    if equity != 0:
        ratios_data.append({"Ratio": "Debt to Equity Ratio", "Value": f"{(total_liabilities / equity):.2f}"})
    if number_of_shares != 0:
        ratios_data.append({"Ratio": "Earnings per Share (EPS)", "Value": f"{(net_income / number_of_shares):.2f}"})

    # Liquidity Ratios
    if total_deposits != 0:
        ratios_data.append({"Ratio": "Loan-to-Deposit Ratio (LDR)", "Value": f"{(total_loans / total_deposits) * 100:.2f}%"})
    if net_cash_outflows_30d != 0:
        ratios_data.append({"Ratio": "Liquidity Coverage Ratio (LCR)", "Value": f"{(high_quality_liquid_assets / net_cash_outflows_30d) * 100:.2f}%"})
    if required_stable_funding != 0:
        ratios_data.append({"Ratio": "Net Stable Funding Ratio (NSFR)", "Value": f"{(available_stable_funding / required_stable_funding) * 100:.2f}%"})

    # Asset Quality Ratios
    if total_loans != 0:
        ratios_data.append({"Ratio": "Non-Performing Loan Ratio (NPL)", "Value": f"{(non_performing_loans / total_loans) * 100:.2f}%"})
        ratios_data.append({"Ratio": "Loan Loss Reserve Ratio (LLR)", "Value": f"{(loan_loss_reserves / total_loans) * 100:.2f}%"})

    # Efficiency Ratios
    if average_earning_assets != 0:
        ratios_data.append({"Ratio": "Net Interest Margin (NIM)", "Value": f"{(operating_income / average_earning_assets) * 100:.2f}%"})
    if operating_income != 0:
        ratios_data.append({"Ratio": "Cost-to-Income Ratio (CIR)", "Value": f"{(staff_costs / operating_income) * 100:.2f}%"})

    # Capital Adequacy Ratios
    if risk_weighted_assets != 0:
        ratios_data.append({"Ratio": "Capital Adequacy Ratio (CAR)", "Value": f"{((tier_1_capital + tier_2_capital) / risk_weighted_assets) * 100:.2f}%"})

    # Market Risk Ratios
    if capital_base != 0:
        ratios_data.append({"Ratio": "Net Open Position (FX) to Capital", "Value": f"{(net_open_position / capital_base) * 100:.2f}%"})

    # Market Performance Ratios
    if number_of_shares != 0:
        ratios_data.append({"Ratio": "Dividend per Share (DPS)", "Value": f"{(dividends / number_of_shares):.2f}"})
    if book_value_per_share != 0:
        ratios_data.append({"Ratio": "Price to Book Ratio (P/B)", "Value": f"{(book_value_per_share):.2f}"})

    # Growth Ratios
    ratios_data.append({"Ratio": "Deposit Growth (%)", "Value": f"{deposit_growth:.2f}%"})
    ratios_data.append({"Ratio": "Loan Growth (%)", "Value": f"{loan_growth:.2f}%"})

    # Display results
    st.subheader("📊 Ratios & Cash Flow Results")
    df = pd.DataFrame(ratios_data)
    st.dataframe(df)

    # Download button for Excel
    towrite = BytesIO()
    df.to_excel(towrite, index=False, sheet_name='Ratios')
    towrite.seek(0)
    st.download_button("📥 Download Results as Excel", data=towrite, file_name=f"{company}_ratios.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
