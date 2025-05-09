#New features added

import streamlit as st
import pandas as pd
from io import BytesIO

# Simple login system
def check_login(username, password):
    return username == "chumcred" and password == "1234"

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.title("🔐 Login to Financial Dashboard")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_clicked = st.button("Login")

    if login_clicked:
        if check_login(username, password):
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            st.error("❌ Invalid username or password.")

if st.session_state["logged_in"]:
    st.title("📊 Financial Ratio & Cash Flow Dashboard")

    company = st.text_input("Company Name", "")

    revenue = st.number_input("Revenue", min_value=0.0, value=0.0)
    cost_of_goods_sold = st.number_input("Cost of Goods Sold", min_value=0.0, value=0.0)
    operating_profit = st.number_input("Operating Profit", min_value=0.0, value=0.0)
    net_income = st.number_input("Net Income", min_value=0.0, value=0.0)
    total_assets = st.number_input("Total Assets", min_value=0.0, value=0.0)
    total_liabilities = st.number_input("Total Liabilities", min_value=0.0, value=0.0)
    equity = st.number_input("Equity", min_value=0.0, value=0.0)
    number_of_shares = st.number_input("Number of Shares Outstanding", min_value=0.0, value=0.0)

    current_assets = st.number_input("Current Assets", min_value=0.0, value=0.0)
    current_liabilities = st.number_input("Current Liabilities", min_value=0.0, value=0.0)
    inventory = st.number_input("Inventory", min_value=0.0, value=0.0)
    cash = st.number_input("Cash", min_value=0.0, value=0.0)

    operating_cash_flow = st.number_input("Operating Cash Flow", min_value=0.0, value=0.0)
    investing_cash_flow = st.number_input("Investing Cash Flow", value=0.0)
    financing_cash_flow = st.number_input("Financing Cash Flow", value=0.0)

    st.subheader("Additional Banking Inputs")
    total_loans = st.number_input("Total Loans", min_value=0.0, value=0.0)
    total_deposits = st.number_input("Total Deposits", min_value=0.0, value=0.0)
    hq_liquid_assets = st.number_input("High-Quality Liquid Assets", min_value=0.0, value=0.0)
    net_cash_outflows_30d = st.number_input("Net Cash Outflows (30 days)", min_value=0.0, value=0.0)
    available_stable_funding = st.number_input("Available Stable Funding", min_value=0.0, value=0.0)
    required_stable_funding = st.number_input("Required Stable Funding", min_value=0.0, value=0.0)
    non_performing_loans = st.number_input("Non-Performing Loans", min_value=0.0, value=0.0)
    staff_costs = st.number_input("Staff Costs", min_value=0.0, value=0.0)
    tier1_capital = st.number_input("Tier 1 Capital", min_value=0.0, value=0.0)
    tier2_capital = st.number_input("Tier 2 Capital", min_value=0.0, value=0.0)
    risk_weighted_assets = st.number_input("Risk-Weighted Assets", min_value=0.0, value=0.0)
    dividends = st.number_input("Dividends Paid", min_value=0.0, value=0.0)
    net_interest_income = st.number_input("Net Interest Income", min_value=0.0, value=0.0)
    avg_earning_assets = st.number_input("Average Earning Assets", min_value=0.0, value=0.0)
    net_open_position = st.number_input("Net Open Position", min_value=0.0, value=0.0)
    capital_base = st.number_input("Capital Base", min_value=0.0, value=0.0)

    if st.button("📈 Calculate Ratios & Cash Flows"):

        gross_profit = revenue - cost_of_goods_sold
        net_cash_flow = operating_cash_flow + investing_cash_flow + financing_cash_flow

        ratios_data = []

        def add_ratio(name, value, analysis, implication, advice):
            ratios_data.append({
                "Ratio": name,
                "Value": f"{value:.2f}" if isinstance(value, (int, float)) else value,
                "Analysis": analysis,
                "Implication": implication,
                "Advice": advice
            })

        # Cash Flow Ratios
        add_ratio("Operating Cash Flow", operating_cash_flow, "Cash from operations.", "Positive is good.", "Focus on improving operational cash.")
        add_ratio("Investing Cash Flow", investing_cash_flow, "Investments cash.", "Negative for growth firms.", "Monitor large investments.")
        add_ratio("Financing Cash Flow", financing_cash_flow, "Cash from financing.", "Positive indicates raised capital.", "Balance debt-equity financing.")
        add_ratio("Net Cash Flow", net_cash_flow, "Net movement of cash.", "Positive is healthy.", "Sustain positive cash flow.")

        # Profitability Ratios
        if revenue:
            add_ratio("Gross Profit Margin (%)", (gross_profit / revenue) * 100, "Production profitability.", "High indicates pricing power.", "Control COGS.")
            add_ratio("Operating Profit Margin (%)", (operating_profit / revenue) * 100, "Core operations profitability.", "High is efficient.", "Control operating expenses.")
            add_ratio("Net Profit Margin (%)", (net_income / revenue) * 100, "Overall profitability.", "Higher is better.", "Boost revenue or cut expenses.")

        # Liquidity Ratios
        if current_liabilities:
            add_ratio("Current Ratio", current_assets / current_liabilities, "Short-term solvency.", "Above 1 is safe.", "Improve cash and current assets.")
            add_ratio("Quick Ratio", (current_assets - inventory) / current_liabilities, "Liquidity without inventory.", "Above 1 is safe.", "Reduce inventory reliance.")

        # Leverage Ratios
        if total_assets:
            add_ratio("Debt to Asset Ratio", total_liabilities / total_assets, "Proportion of debt in assets.", "Lower is safer.", "Reduce liabilities.")
        if equity:
            add_ratio("Debt to Equity Ratio", total_liabilities / equity, "Leverage level.", "Lower is safer.", "Improve equity base.")

        # Banking-specific Ratios
        if total_loans:
            add_ratio("Non-Performing Loan Ratio (%)", (non_performing_loans / total_loans) * 100, "Credit quality.", "Lower is better.", "Tighten credit policies.")
        if net_cash_outflows_30d:
            add_ratio("Liquidity Coverage Ratio (%)", (hq_liquid_assets / net_cash_outflows_30d) * 100, "Liquidity in stress.", "Above 100% is safe.", "Increase liquid assets.")
        if required_stable_funding:
            add_ratio("Net Stable Funding Ratio (%)", (available_stable_funding / required_stable_funding) * 100, "Long-term funding stability.", "Above 100% is ideal.", "Boost stable funding.")
        if risk_weighted_assets:
            add_ratio("Capital Adequacy Ratio (%)", ((tier1_capital + tier2_capital) / risk_weighted_assets) * 100, "Capital buffer.", "Above regulatory min.", "Increase capital.")
        if avg_earning_assets:
            add_ratio("Net Interest Margin (%)", (net_interest_income / avg_earning_assets) * 100, "Interest profitability.", "Higher is better.", "Boost interest income or optimize funding.")
        if capital_base:
            add_ratio("Net Open Position to Capital (%)", (net_open_position / capital_base) * 100, "FX risk exposure.", "Lower is safer.", "Hedge FX risks.")

        df = pd.DataFrame(ratios_data)
        st.dataframe(df)

        output = BytesIO()
        df.to_csv(output, index=False)
        csv_data = output.getvalue()

        st.download_button(
            label="📥 Download Ratios as CSV",
            data=csv_data,
            file_name=f"{company}_ratios.csv",
            mime="text/csv"
        )
