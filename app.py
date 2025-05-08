import streamlit as st
import pandas as pd
from io import BytesIO

# Simple admin authentication
def check_password():
    def password_entered():
        if (st.session_state["username"] == "admin"
                and st.session_state["password"] == "12345"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        st.button("Login", on_click=password_entered)
        return False
    elif not st.session_state["password_correct"]:
        st.error("Invalid credentials")
        return False
    else:
        return True

if check_password():
    st.title("📊 Financial Ratio & Cash Flow Calculator")

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

    operating_cash_flow = st.number_input("Operating Cash Flow", min_value=0.0, value=0.0)
    investing_cash_flow = st.number_input("Investing Cash Flow", min_value=0.0, value=0.0)
    financing_cash_flow = st.number_input("Financing Cash Flow", min_value=0.0, value=0.0)

    # Banking-specific inputs
    st.subheader("📌 Banking & Financial Institution Inputs")
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

    # Ratio calculations
    ratios = {}

    try:
        ratios["Gross Profit Margin (%)"] = ((revenue - cost_of_goods_sold) / revenue) * 100 if revenue else 0
        ratios["Net Profit Margin (%)"] = (net_income / revenue) * 100 if revenue else 0
        ratios["Operating Profit Margin (%)"] = (operating_profit / revenue) * 100 if revenue else 0
        ratios["Return on Assets (ROA) (%)"] = (net_income / total_assets) * 100 if total_assets else 0
        ratios["Return on Equity (ROE) (%)"] = (net_income / equity) * 100 if equity else 0
        ratios["Debt to Equity Ratio"] = (total_liabilities / equity) if equity else 0
        ratios["Earnings per Share (EPS)"] = (net_income / number_of_shares) if number_of_shares else 0
        ratios["Loan-to-Deposit Ratio (LDR) (%)"] = (total_loans / total_deposits) * 100 if total_deposits else 0
        ratios["Liquidity Coverage Ratio (LCR) (%)"] = (high_quality_liquid_assets / net_cash_outflows_30d) * 100 if net_cash_outflows_30d else 0
        ratios["Net Stable Funding Ratio (NSFR) (%)"] = (available_stable_funding / required_stable_funding) * 100 if required_stable_funding else 0
        ratios["Non-Performing Loan (NPL) Ratio (%)"] = (non_performing_loans / total_loans) * 100 if total_loans else 0
        ratios["Cost-to-Income Ratio (%)"] = (staff_costs / operating_income) * 100 if operating_income else 0
        ratios["Capital Adequacy Ratio (CAR) (%)"] = ((tier1_capital + tier2_capital) / risk_weighted_assets) * 100 if risk_weighted_assets else 0
        ratios["Leverage Ratio (%)"] = (tier1_capital / total_assets_bank) * 100 if total_assets_bank else 0
        ratios["Dividend Payout Ratio (%)"] = (dividends / net_income) * 100 if net_income else 0
        ratios["Net Interest Margin (NIM) (%)"] = (net_interest_income / average_earning_assets) * 100 if average_earning_assets else 0
        ratios["Forex Exposure Ratio (%)"] = (net_open_position / capital_base) * 100 if capital_base else 0
        ratios["Book Value per Share"] = (book_value / number_of_shares) if number_of_shares else 0
    except ZeroDivisionError:
        st.error("Division by zero encountered in calculation.")

    st.subheader("📈 Financial Ratios")
    st.write(pd.DataFrame.from_dict(ratios, orient='index', columns=["Value (%)"]).round(2))

    # Download as Excel
    if st.button("📥 Download Results as Excel"):
        output = BytesIO()
        df = pd.DataFrame.from_dict(ratios, orient='index', columns=["Value (%)"]).round(2)
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Financial Ratios')
        st.download_button(label="Download Excel File", data=output.getvalue(), file_name=f"{company}_financial_ratios.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

