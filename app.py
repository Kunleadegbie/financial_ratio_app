#This should be the last Script

import streamlit as st
import pandas as pd

# Title
st.title("📊 Financial & Banking Ratios Dashboard")

# Input Sections
company = st.text_input("Company Name")

st.subheader("📑 Financial Data")
revenue = st.number_input("Revenue", 0.0)
cost_of_goods_sold = st.number_input("Cost of Goods Sold", 0.0)
operating_profit = st.number_input("Operating Profit", 0.0)
net_income = st.number_input("Net Income", 0.0)
total_assets = st.number_input("Total Assets", 0.0)
total_liabilities = st.number_input("Total Liabilities", 0.0)
equity = st.number_input("Equity", 0.0)
number_of_shares = st.number_input("Number of Shares", 0.0)
operating_income = st.number_input("Operating Income", 0.0)
staff_costs = st.number_input("Staff Costs", 0.0)
book_value_per_share = st.number_input("Book Value Per Share", 0.0)

st.subheader("🏦 Banking Data")
total_loans = st.number_input("Total Loans", 0.0)
total_deposits = st.number_input("Total Deposits", 0.0)
non_performing_loans = st.number_input("Non-Performing Loans", 0.0)
loan_loss_reserves = st.number_input("Loan Loss Reserves", 0.0)
average_earning_assets = st.number_input("Average Earning Assets", 0.0)
tier_1_capital = st.number_input("Tier 1 Capital", 0.0)
tier_2_capital = st.number_input("Tier 2 Capital", 0.0)
capital_base = st.number_input("Capital Base", 0.0)
risk_weighted_assets = st.number_input("Risk-Weighted Assets", 0.0)
net_open_position = st.number_input("Net Open Position (FX)", 0.0)
dividends = st.number_input("Dividends Paid", 0.0)
deposit_growth = st.number_input("Deposit Growth (%)", 0.0)
loan_growth = st.number_input("Loan Growth (%)", 0.0)
market_price_per_share = st.number_input("Market Price Per Share", 0.0)

# Button to calculate ratios
if st.button("📈 Calculate Ratios"):
    ratios = []

    try:
        # Profitability
        if revenue:
            gross_profit = revenue - cost_of_goods_sold
            ratios.append({"Ratio": "Gross Profit Margin", "Value": f"{(gross_profit/revenue)*100:.2f}%"})
            ratios.append({"Ratio": "Net Profit Margin", "Value": f"{(net_income/revenue)*100:.2f}%"})
            ratios.append({"Ratio": "Operating Profit Margin", "Value": f"{(operating_profit/revenue)*100:.2f}%"})
        if total_assets:
            ratios.append({"Ratio": "Return on Assets (ROA)", "Value": f"{(net_income/total_assets)*100:.2f}%"})
        if equity:
            ratios.append({"Ratio": "Return on Equity (ROE)", "Value": f"{(net_income/equity)*100:.2f}%"})
        if number_of_shares:
            ratios.append({"Ratio": "Earnings Per Share (EPS)", "Value": f"{(net_income/number_of_shares):.2f}"})

        # Banking Ratios
        if total_deposits:
            ratios.append({"Ratio": "Loan-to-Deposit Ratio", "Value": f"{(total_loans/total_deposits)*100:.2f}%"})
        if total_loans:
            ratios.append({"Ratio": "Non-Performing Loan (NPL) Ratio", "Value": f"{(non_performing_loans/total_loans)*100:.2f}%"})
            ratios.append({"Ratio": "Loan Loss Reserve (LLR) Ratio", "Value": f"{(loan_loss_reserves/total_loans)*100:.2f}%"})
        if average_earning_assets:
            ratios.append({"Ratio": "Net Interest Margin (NIM)", "Value": f"{(operating_income/average_earning_assets)*100:.2f}%"})
        if operating_income:
            ratios.append({"Ratio": "Cost-to-Income Ratio", "Value": f"{(staff_costs/operating_income)*100:.2f}%"})
        if risk_weighted_assets:
            ratios.append({"Ratio": "Capital Adequacy Ratio (CAR)", "Value": f"{(capital_base/risk_weighted_assets)*100:.2f}%"})
            ratios.append({"Ratio": "Tier 1 Capital Ratio", "Value": f"{(tier_1_capital/risk_weighted_assets)*100:.2f}%"})
        if capital_base:
            ratios.append({"Ratio": "FX Net Open Position Limit", "Value": f"{(net_open_position/capital_base)*100:.2f}%"})
        if net_income:
            ratios.append({"Ratio": "Dividend Payout Ratio", "Value": f"{(dividends/net_income)*100:.2f}%"})

        # Growth Rates
        ratios.append({"Ratio": "Deposit Growth Rate", "Value": f"{deposit_growth:.2f}%"})
        ratios.append({"Ratio": "Loan Growth Rate", "Value": f"{loan_growth:.2f}%"})

        # Valuation
        if book_value_per_share:
            ratios.append({"Ratio": "Price-to-Book (P/B) Ratio", "Value": f"{(market_price_per_share/book_value_per_share):.2f}"})

        # Convert to DataFrame and display
        ratio_df = pd.DataFrame(ratios)
        st.subheader("📊 Computed Ratios")
        st.dataframe(ratio_df)

    except Exception as e:
        st.error(f"Error calculating ratios: {e}")
