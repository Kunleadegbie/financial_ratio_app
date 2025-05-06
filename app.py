import streamlit as st
import pandas as pd
from io import BytesIO

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

# Additional Bank-specific inputs
st.subheader("📌 Additional Banking & Financial Institution Inputs")

total_loans = st.number_input("Total Loans", min_value=0.0, value=0.0)
total_deposits = st.number_input("Total Deposits", min_value=0.0, value=0.0)
high_quality_liquid_assets = st.number_input("High-Quality Liquid Assets", min_value=0.0, value=0.0)
net_cash_outflows_30d = st.number_input("Total Net Cash Outflows (30 days)", min_value=0.0, value=0.0)
available_stable_funding = st.number_input("Available Stable Funding", min_value=0.0, value=0.0)
required_stable_funding = st.number_input("Required Stable Funding", min_value=0.0, value=0.0)
non_performing_loans = st.number_input("Non-Performing Loans", min_value=0.0, value=0.0)
loan_loss_reserves = st.number_input("Loan Loss Reserves", min_value=0.0, value=0.0)
net_interest_income = st.number_input("Net Interest Income", min_value=0.0, value=0.0)
average_earning_assets = st.number_input("Average Earning Assets", min_value=0.0, value=0.0)
operating_income = st.number_input("Operating Income", min_value=0.0, value=0.0)
staff_costs = st.number_input("Staff Costs", min_value=0.0, value=0.0)
tier1_capital = st.number_input("Tier 1 Capital", min_value=0.0, value=0.0)
tier2_capital = st.number_input("Tier 2 Capital", min_value=0.0, value=0.0)
risk_weighted_assets = st.number_input("Risk-Weighted Assets", min_value=0.0, value=0.0)
total_assets_bank = st.number_input("Total Assets (for Leverage Ratio)", min_value=0.0, value=0.0)
dividends = st.number_input("Dividends", min_value=0.0, value=0.0)
net_open_position = st.number_input("Net Open Position (Forex Exposure)", min_value=0.0, value=0.0)
capital_base = st.number_input("Capital Base (for Forex Exposure)", min_value=0.0, value=0.0)
book_value = st.number_input("Book Value", min_value=0.0, value=0.0)

# Button to calculate ratios
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

    if equity:
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
        ratios_data.append({"Ratio": "Loan Loss Reserve to Gross Loans", "Value": f"{(loan_loss_reserves / total_loans) * 100:.2f}%"})

    if non_performing_loans:
        ratios_data.append({"Ratio": "Provision Coverage Ratio", "Value": f"{(loan_loss_reserves / non_performing_loans) * 100:.2f}%"})

    if average_earning_assets:
        ratios_data.append({"Ratio": "Net Interest Margin (NIM)", "Value": f"{(net_interest_income / average_earning_assets) * 100:.2f}%"})

    if operating_income:
        ratios_data.append({"Ratio": "Cost-to-Income Ratio", "Value": f"{(operating_profit / operating_income) * 100:.2f}%"})
        ratios_data.append({"Ratio": "Staff Cost to Income Ratio", "Value": f"{(staff_costs / operating_income) * 100:.2f}%"})

    if risk_weighted_assets:
        ratios_data.append({"Ratio": "Capital Adequacy Ratio (CAR)", "Value": f"{((tier1_capital + tier2_capital) / risk_weighted_assets) * 100:.2f}%"})
        ratios_data.append({"Ratio": "Tier 1 Capital Ratio", "Value": f"{(tier1_capital / risk_weighted_assets) * 100:.2f}%"})

    if total_assets_bank:
        ratios_data.append({"Ratio": "Leverage Ratio", "Value": f"{(tier1_capital / total_assets_bank) * 100:.2f}%"})

    if capital_base:
        ratios_data.append({"Ratio": "Foreign Exchange Exposure Ratio", "Value": f"{(net_open_position / capital_base) * 100:.2f}%"})

    if net_income:
        ratios_data.append({"Ratio": "Dividend Payout Ratio", "Value": f"{(dividends / net_income) * 100:.2f}%"})

    if number_of_shares:
        ratios_data.append({"Ratio": "Book Value per Share", "Value": f"{(book_value / number_of_shares):.2f}"})

    # Convert to DataFrame
    ratios_df = pd.DataFrame(ratios_data)

    # Display results
    st.subheader(f"📊 Financial Ratios for {company if company else 'the Company'}")
    st.dataframe(ratios_df)

    # CSV Export
    csv_buffer = BytesIO()
    ratios_df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    st.download_button(
        label="📥 Download Ratios as CSV",
        data=csv_buffer,
        file_name=f"{company.replace(' ', '_')}_financial_ratios.csv" if company else "financial_ratios.csv",
        mime="text/csv"
    )
