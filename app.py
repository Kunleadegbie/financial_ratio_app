import streamlit as st
import pandas as pd

st.title("📊 Financial Ratio & Cash Flow Analyzer")

# --- Company Name ---
company = st.text_input("🏢 Company Name", "")

# --- General Financial Data Inputs ---
st.subheader("📃 General Financial Data")
revenue = st.number_input("Revenue", min_value=0.0, value=0.0)
cost_of_goods_sold = st.number_input("Cost of Goods Sold", min_value=0.0, value=0.0)
operating_profit = st.number_input("Operating Profit", min_value=0.0, value=0.0)
net_income = st.number_input("Net Income", min_value=0.0, value=0.0)
total_assets = st.number_input("Total Assets", min_value=0.0, value=0.0)
total_liabilities = st.number_input("Total Liabilities", min_value=0.0, value=0.0)
equity = st.number_input("Equity", min_value=0.0, value=0.0)
number_of_shares = st.number_input("Number of Shares Outstanding", min_value=0.0, value=0.0)

# --- Cash Flow Data ---
st.subheader("💵 Cash Flow Data")
operating_cash_flow = st.number_input("Operating Cash Flow", min_value=0.0, value=0.0)
investing_cash_flow = st.number_input("Investing Cash Flow", min_value=0.0, value=0.0)
financing_cash_flow = st.number_input("Financing Cash Flow", min_value=0.0, value=0.0)

# --- Banking/Financial Institution Data ---
st.subheader("🏦 Banking & Financial Institution Data")
total_loans = st.number_input("Total Loans", min_value=0.0, value=0.0)
total_deposits = st.number_input("Total Deposits", min_value=0.0, value=0.0)
non_performing_loans = st.number_input("Non-Performing Loans", min_value=0.0, value=0.0)
loan_loss_reserves = st.number_input("Loan Loss Reserves", min_value=0.0, value=0.0)
average_earning_assets = st.number_input("Average Earning Assets", min_value=0.0, value=0.0)
operating_income = st.number_input("Operating Income", min_value=0.0, value=0.0)
staff_costs = st.number_input("Staff Costs", min_value=0.0, value=0.0)
tier_1_capital = st.number_input("Tier 1 Capital", min_value=0.0, value=0.0)
tier_2_capital = st.number_input("Tier 2 Capital", min_value=0.0, value=0.0)
capital_base = st.number_input("Capital Base", min_value=0.0, value=0.0)
risk_weighted_assets = st.number_input("Risk-Weighted Assets", min_value=0.0, value=0.0)
net_open_position = st.number_input("Net Open Position (FX)", min_value=0.0, value=0.0)
dividends = st.number_input("Dividends Paid", min_value=0.0, value=0.0)
deposit_growth = st.number_input("Deposit Growth (%)", min_value=0.0, value=0.0)
loan_growth = st.number_input("Loan Growth (%)", min_value=0.0, value=0.0)

# --- Market & Valuation Data ---
st.subheader("📈 Valuation Data")
market_price_per_share = st.number_input("Market Price Per Share", min_value=0.0, value=0.0)
book_value_per_share = st.number_input("Book Value Per Share", min_value=0.0, value=0.0)

# --- Calculate Ratios & Cash Flows ---
if st.button("📊 Calculate Ratios & Cash Flows"):
    gross_profit = revenue - cost_of_goods_sold
    ratios_data = []

    # Cash Flows
    ratios_data.extend([
        {"Ratio": "Operating Cash Flow", "Value": f"{operating_cash_flow:.2f}"},
        {"Ratio": "Investing Cash Flow", "Value": f"{investing_cash_flow:.2f}"},
        {"Ratio": "Financing Cash Flow", "Value": f"{financing_cash_flow:.2f}"},
    ])

    # Profitability Ratios
    if revenue:
        ratios_data.extend([
            {"Ratio": "Gross Profit Margin", "Value": f"{(gross_profit / revenue) * 100:.2f}%"},
            {"Ratio": "Net Profit Margin", "Value": f"{(net_income / revenue) * 100:.2f}%"},
            {"Ratio": "Operating Profit Margin", "Value": f"{(operating_profit / revenue) * 100:.2f}%"}
        ])

    # Return Ratios
    if total_assets:
        ratios_data.append({"Ratio": "Return on Assets (ROA)", "Value": f"{(net_income / total_assets) * 100:.2f}%"})

    if equity:
        ratios_data.append({"Ratio": "Return on Equity (ROE)", "Value": f"{(net_income / equity) * 100:.2f}%"})

    # Leverage
    if total_liabilities and equity:
        ratios_data.append({"Ratio": "Debt to Equity Ratio", "Value": f"{(total_liabilities / equity):.2f}"})

    # Per Share
    if number_of_shares:
        ratios_data.append({"Ratio": "Earnings per Share (EPS)", "Value": f"{(net_income / number_of_shares):.2f}"})

    # Banking Ratios
    if total_deposits:
        ratios_data.append({"Ratio": "Loan-to-Deposit Ratio (LDR)", "Value": f"{(total_loans / total_deposits) * 100:.2f}%"})

    if total_loans:
        ratios_data.append({"Ratio": "Non-Performing Loan (NPL) Ratio", "Value": f"{(non_performing_loans / total_loans) * 100:.2f}%"})
        ratios_data.append({"Ratio": "Loan Loss Reserve to Gross Loans", "Value": f"{(loan_loss_reserves / total_loans) * 100:.2f}%"})

    if non_performing_loans:
        ratios_data.append({"Ratio": "Provision Coverage Ratio", "Value": f"{(loan_loss_reserves / non_performing_loans) * 100:.2f}%"})

    if average_earning_assets:
        ratios_data.append({"Ratio": "Net Interest Margin (NIM)", "Value": f"{(net_income / average_earning_assets) * 100:.2f}%"})

    if operating_income:
        ratios_data.append({"Ratio": "Cost-to-Income Ratio", "Value": f"{(operating_profit / operating_income) * 100:.2f}%"})
        ratios_data.append({"Ratio": "Staff Cost to Income Ratio", "Value": f"{(staff_costs / operating_income) * 100:.2f}%"})

    # Display Ratios Table
    df_ratios = pd.DataFrame(ratios_data)
    st.subheader("📊 Calculated Financial Ratios")
    st.dataframe(df_ratios)

    # Download CSV
    csv = df_ratios.to_csv(index=False).encode('utf-8')
    download_filename = f"{company}_financial_ratios.csv" if company else "financial_ratios.csv"

    st.download_button(
        label="📥 Download Ratios as CSV",
        data=csv,
        file_name=download_filename,
        mime='text/csv'
    )
