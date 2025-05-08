import streamlit as st
import pandas as pd
from io import BytesIO

# Simple login system
def check_login(username, password):
    return username == "chumcred" and password == "1234"

# Login inputs
st.title("🔐 Login to Financial Dashboard")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
login_clicked = st.button("Login")

# If login button clicked
if login_clicked:
    if check_login(username, password):
        # App title and header
        st.title("📊 Financial Ratio & Cash Flow Dashboard")
        st.markdown("Input financial figures below to compute key ratios and cash flows.")

        # Company input
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

        # Liquidity data inputs
        current_assets = st.number_input("Current Assets", min_value=0.0, value=0.0)
        current_liabilities = st.number_input("Current Liabilities", min_value=0.0, value=0.0)
        inventory = st.number_input("Inventory", min_value=0.0, value=0.0)
        cash = st.number_input("Cash", min_value=0.0, value=0.0)

        # Cash Flow data
        operating_cash_flow = st.number_input("Operating Cash Flow", min_value=0.0, value=0.0)
        investing_cash_flow = st.number_input("Investing Cash Flow", min_value=0.0, value=0.0)
        financing_cash_flow = st.number_input("Financing Cash Flow", min_value=0.0, value=0.0)

        # Banking & Financial Institution Inputs
        st.subheader("Additional Banking & Financial Institution Inputs")
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

            # Ratios Table
            ratios_data = []

            def add_ratio(name, value, analysis, implication, advice):
                ratios_data.append({
                    "Ratio": name,
                    "Value": f"{value:.2f}" if isinstance(value, (int, float)) else value,
                    "Analysis": analysis,
                    "Implication": implication,
                    "Advice": advice
                })

            # Cash Flows
            add_ratio("Operating Cash Flow", operating_cash_flow, "Cash from core operations.", "Positive figure means good liquidity.", "Maintain or increase operating cash flow.")
            add_ratio("Investing Cash Flow", investing_cash_flow, "Cash from investments.", "Negative is normal for growth firms.", "Monitor major outflows.")
            add_ratio("Financing Cash Flow", financing_cash_flow, "Cash from financing activities.", "Positive indicates capital raised.", "Balance between debt and equity financing.")
            add_ratio("Net Cash Flow", net_cash_flow, "Net movement of cash.", "Positive is healthy.", "Ensure sustained positive cash flow.")

            # Profitability Ratios
            if revenue:
                add_ratio("Gross Profit Margin (%)", (gross_profit / revenue) * 100, "Measures production profitability.", "High margin indicates good pricing power.", "Control COGS to improve margin.")
                add_ratio("Net Profit Margin (%)", (net_income / revenue) * 100, "Overall profitability.", "Higher is better.", "Optimize operational costs.")
                add_ratio("Operating Profit Margin (%)", (operating_profit / revenue) * 100, "Operational efficiency.", "High margin signals operational strength.", "Streamline operational processes.")

            if total_assets:
                add_ratio("Return on Assets (ROA) (%)", (net_income / total_assets) * 100, "Efficiency of asset usage.", "Higher ratio indicates better asset utilization.", "Dispose of underperforming assets.")

            if equity:
                add_ratio("Return on Equity (ROE) (%)", (net_income / equity) * 100, "Return to shareholders.", "Higher ratio is attractive to investors.", "Enhance revenue and control costs.")

            # Liquidity Ratios
            if current_liabilities:
                current_ratio = current_assets / current_liabilities
                quick_ratio = (current_assets - inventory) / current_liabilities
                cash_ratio = cash / current_liabilities

                add_ratio("Current Ratio", current_ratio, "Ability to meet short-term debts.", "Above 1 indicates good liquidity.", "Improve working capital management.")
                add_ratio("Quick Ratio", quick_ratio, "Stringent liquidity test.", "Above 1 is safe.", "Reduce inventory dependency.")
                add_ratio("Cash Ratio", cash_ratio, "Most liquid ratio.", "Closer to 1 is ideal.", "Increase cash reserves if low.")

            # Banking Ratios
            if total_deposits:
                add_ratio("Loan to Deposit Ratio", total_loans / total_deposits, "Credit exposure relative to deposits.", "Above 1 indicates aggressive lending.", "Balance loan portfolio.")

            if net_cash_outflows_30d:
                add_ratio("Liquidity Coverage Ratio (LCR)", hq_liquid_assets / net_cash_outflows_30d, "Liquidity buffer adequacy.", "Above 1 indicates sufficient liquidity.", "Maintain adequate liquid assets.")

            if required_stable_funding:
                add_ratio("Net Stable Funding Ratio (NSFR)", available_stable_funding / required_stable_funding, "Long-term liquidity stability.", "Above 1 is healthy.", "Align funding with asset profiles.")

            if total_loans:
                add_ratio("NPL Ratio", non_performing_loans / total_loans, "Loan quality measure.", "Lower ratio indicates healthier portfolio.", "Reduce non-performing exposures.")

            if operating_profit:
                add_ratio("Cost to Income Ratio", staff_costs / operating_profit, "Operational efficiency.", "Lower ratio is better.", "Control operational expenses.")

            if risk_weighted_assets:
                car = (tier1_capital + tier2_capital) / risk_weighted_assets
                add_ratio("Capital Adequacy Ratio (CAR)", car, "Capital buffer strength.", "Higher ratio signals resilience.", "Maintain adequate capital levels.")

            if total_assets:
                add_ratio("Leverage Ratio", tier1_capital / total_assets, "Core capital to total assets.", "Higher ratio means stronger capital base.", "Increase tier 1 capital.")

            if net_income:
                add_ratio("Dividend Payout Ratio", dividends / net_income, "Earnings distributed as dividends.", "High ratio reduces retained earnings.", "Balance dividend and retention policy.")

            if avg_earning_assets:
                add_ratio("Net Interest Margin (NIM)", net_interest_income / avg_earning_assets, "Interest income efficiency.", "Higher NIM is profitable.", "Optimize asset yield and funding cost.")

            if capital_base:
                add_ratio("Forex Exposure Limit", net_open_position / capital_base, "Foreign exchange exposure control.", "Lower ratio limits risk.", "Hedge excessive forex positions.")

            # Display table
            df = pd.DataFrame(ratios_data)
            st.dataframe(df)

            # CSV download
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Results as CSV", data=csv, file_name=f"{company}_financial_ratios.csv", mime="text/csv")

    else:
        st.error("Invalid login credentials. Please try again.")
