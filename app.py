#added import libraries

import streamlit as st
import pandas as pd

# Any other imports you might have

# Your app logic starts here
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
        add_ratio("Current Ratio", (current_assets / current_liabilities), "Measures short-term liquidity.", "Higher ratio suggests good short-term financial health.", "Maintain adequate current assets.")
        add_ratio("Quick Ratio", ((current_assets - inventory) / current_liabilities), "Liquidity excluding inventory.", "Higher is better.", "Improve quick assets.")
        add_ratio("Cash Ratio", (cash / current_liabilities), "Strictest liquidity test.", "Higher indicates strong liquidity.", "Maintain sufficient cash reserves.")

    # Leverage / Solvency Ratios
    if equity:
        add_ratio("Debt to Equity Ratio", (total_liabilities / equity), "Measures leverage.", "Lower ratio is safer.", "Reduce liabilities or increase equity.")

    if total_assets:
        add_ratio("Debt Ratio", (total_liabilities / total_assets), "Proportion of assets financed by debt.", "Lower ratio is preferable.", "Manage liabilities carefully.")

    # Additional Banking & Financial Institution Ratios
    if total_deposits:
        add_ratio("Loan to Deposit Ratio (%)", (total_loans / total_deposits) * 100, "Credit exposure relative to deposits.", "Higher ratio indicates aggressive lending.", "Monitor loan portfolio.")

    if net_cash_outflows_30d:
        add_ratio("Liquidity Coverage Ratio (LCR)", (hq_liquid_assets / net_cash_outflows_30d) * 100, "Ability to cover short-term outflows.", "Higher ratio suggests better liquidity.", "Maintain high-quality liquid assets.")

    if required_stable_funding:
        add_ratio("Net Stable Funding Ratio (NSFR)", (available_stable_funding / required_stable_funding) * 100, "Long-term liquidity indicator.", "Higher ratio indicates funding stability.", "Secure long-term funding sources.")

    if risk_weighted_assets:
        capital_adequacy_ratio = ((tier1_capital + tier2_capital) / risk_weighted_assets) * 100
        add_ratio("Capital Adequacy Ratio (CAR)", capital_adequacy_ratio, "Bank's risk resilience.", "Higher is safer.", "Maintain adequate capital buffers.")

    if total_loans:
        add_ratio("Non-Performing Loan (NPL) Ratio (%)", (non_performing_loans / total_loans) * 100, "Quality of loan portfolio.", "Lower ratio is healthier.", "Improve credit risk controls.")

    if net_interest_income:
        add_ratio("Cost to Income Ratio (%)", (staff_costs / net_interest_income) * 100, "Operational efficiency.", "Lower ratio indicates cost efficiency.", "Control operating expenses.")

    if avg_earning_assets:
        add_ratio("Net Interest Margin (NIM) (%)", (net_interest_income / avg_earning_assets) * 100, "Profitability of earning assets.", "Higher margin is better.", "Enhance interest income.")

    if capital_base:
        add_ratio("Open Position to Capital Base (%)", (net_open_position / capital_base) * 100, "FX risk exposure.", "Lower ratio reduces risk.", "Limit open currency positions.")

    # Display Ratios in DataFrame
    st.subheader(f"📊 Financial Ratios for {company}")
    df = pd.DataFrame(ratios_data)
    st.dataframe(df)

    # Download CSV
    csv = df.to_csv(index=False).encode()
    st.download_button("📥 Download Ratios as CSV", data=csv, file_name=f"{company}_financial_ratios.csv", mime='text/csv')
