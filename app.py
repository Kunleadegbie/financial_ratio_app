import streamlit as st
import pandas as pd
import os
from datetime import datetime
from io import BytesIO

# Create results directory if it doesn't exist
if not os.path.exists("results"):
    os.makedirs("results")

# Custom CSS for clean styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .block-container {
        padding-top: 2rem;
    }
    .stButton>button {
        background-color: #1a73e8;
        color: white;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #155ab6;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("CHUMCRED ACADEMY Financial Ratio Calculator")

# User login section
st.sidebar.header("User Login")
name = st.sidebar.text_input("Full Name")
email = st.sidebar.text_input("Email")
company = st.sidebar.text_input("Company Name (optional)")

if name and email:
    st.sidebar.success(f"Welcome {name}! Start your calculation below.")

    st.header("Enter Financial Figures")

    st.subheader("Liquidity Ratios")
    current_assets = st.number_input("Current Assets", min_value=0.0)
    current_liabilities = st.number_input("Current Liabilities", min_value=0.0)
    inventory = st.number_input("Inventory", min_value=0.0)
    cash = st.number_input("Cash & Cash Equivalents", min_value=0.0)

    st.subheader("Profitability Ratios")
    gross_profit = st.number_input("Gross Profit", min_value=0.0)
    net_income = st.number_input("Net Income", min_value=0.0)
    revenue = st.number_input("Revenue", min_value=0.0)
    total_assets = st.number_input("Total Assets", min_value=0.0)
    equity = st.number_input("Equity", min_value=0.0)
    operating_profit = st.number_input("Operating Profit", min_value=0.0)

    st.subheader("Solvency Ratios")
    total_liabilities = st.number_input("Total Liabilities", min_value=0.0)
    interest_expense = st.number_input("Interest Expense", min_value=0.0)

    st.subheader("Efficiency Ratios")
    cost_of_goods_sold = st.number_input("Cost of Goods Sold", min_value=0.0)
    average_inventory = st.number_input("Average Inventory", min_value=0.0)
    accounts_receivable = st.number_input("Accounts Receivable", min_value=0.0)
    average_receivable = st.number_input("Average Accounts Receivable", min_value=0.0)
    average_payable = st.number_input("Average Accounts Payable", min_value=0.0)
    accounts_payable = st.number_input("Accounts Payable", min_value=0.0)

    st.subheader("Market Value Ratios")
    earnings_per_share = st.number_input("Earnings Per Share (EPS)", min_value=0.0)
    market_price_per_share = st.number_input("Market Price per Share", min_value=0.0)
    dividend_per_share = st.number_input("Dividend per Share", min_value=0.0)

    if st.button("Calculate Ratios"):
        results = []

        def analyze_ratio(ratio_name, value, thresholds):
            if value is None:
                return
            for condition, analysis, implication, advice in thresholds:
                if condition(value):
                    return {
                        'Ratio': ratio_name,
                        'Value': round(value, 2),
                        'Analysis': analysis,
                        'Implication': implication,
                        'Advice': advice
                    }

        if current_liabilities:
            current_ratio = current_assets / current_liabilities
            results.append(analyze_ratio("Current Ratio", current_ratio, [
                (lambda x: x >= 2, "Healthy", "Can meet short-term obligations", "Maintain liquidity levels."),
                (lambda x: x < 2, "Weak", "Struggle to cover short-term debts", "Increase liquid assets.")
            ]))

            quick_ratio = (current_assets - inventory) / current_liabilities
            results.append(analyze_ratio("Quick Ratio", quick_ratio, [
                (lambda x: x >= 1, "Healthy", "Quick assets cover liabilities", "Good financial health."),
                (lambda x: x < 1, "Weak", "Insufficient liquid assets", "Increase cash or receivables.")
            ]))

            cash_ratio = cash / current_liabilities
            results.append(analyze_ratio("Cash Ratio", cash_ratio, [
                (lambda x: x >= 0.5, "Safe", "Enough cash for immediate needs", "Solid position."),
                (lambda x: x < 0.5, "Low", "Limited immediate liquidity", "Boost cash reserves.")
            ]))

        if revenue:
            gross_margin = gross_profit / revenue
            results.append(analyze_ratio("Gross Profit Margin", gross_margin, [
                (lambda x: x >= 0.4, "High", "Strong cost control", "Maintain pricing and costs."),
                (lambda x: x < 0.4, "Low", "Poor cost control", "Review production costs.")
            ]))

            net_margin = net_income / revenue
            results.append(analyze_ratio("Net Profit Margin", net_margin, [
                (lambda x: x >= 0.1, "Profitable", "Good operational efficiency", "Sustain profit levels."),
                (lambda x: x < 0.1, "Weak", "Low profitability", "Cut unnecessary expenses.")
            ]))

        if total_assets:
            roa = net_income / total_assets
            results.append(analyze_ratio("Return on Assets (ROA)", roa, [
                (lambda x: x >= 0.05, "Good", "Efficient use of assets", "Maintain asset productivity."),
                (lambda x: x < 0.05, "Poor", "Underperforming assets", "Improve asset management.")
            ]))

        if equity:
            roe = net_income / equity
            results.append(analyze_ratio("Return on Equity (ROE)", roe, [
                (lambda x: x >= 0.15, "Strong", "Good shareholder returns", "Maintain capital efficiency."),
                (lambda x: x < 0.15, "Low", "Weak shareholder value", "Boost profitability.")
            ]))

        if equity:
            debt_equity = total_liabilities / equity
            results.append(analyze_ratio("Debt-to-Equity Ratio", debt_equity, [
                (lambda x: x <= 2, "Balanced", "Acceptable leverage", "Maintain capital structure."),
                (lambda x: x > 2, "High", "Risky financial leverage", "Reduce debt levels.")
            ]))

        if interest_expense:
            interest_cover = operating_profit / interest_expense
            results.append(analyze_ratio("Interest Coverage Ratio", interest_cover, [
                (lambda x: x >= 3, "Safe", "Able to meet interest payments", "Solid debt management."),
                (lambda x: x < 3, "At Risk", "Debt servicing risk", "Boost operating profits.")
            ]))

        if average_inventory:
            inventory_turnover = cost_of_goods_sold / average_inventory
            results.append(analyze_ratio("Inventory Turnover", inventory_turnover, [
                (lambda x: x >= 5, "Efficient", "Strong inventory management", "Maintain turnover."),
                (lambda x: x < 5, "Weak", "Excess stock held", "Review inventory policies.")
            ]))

        if average_receivable:
            receivable_turnover = revenue / average_receivable
            results.append(analyze_ratio("Receivables Turnover", receivable_turnover, [
                (lambda x: x >= 5, "Efficient", "Fast debt collection", "Sustain collection efforts."),
                (lambda x: x < 5, "Slow", "Slow debt recovery", "Tighten credit policy.")
            ]))

        if average_payable:
            payable_turnover = cost_of_goods_sold / average_payable
            results.append(analyze_ratio("Payables Turnover", payable_turnover, [
                (lambda x: x >= 5, "Prompt", "Quick supplier payments", "Consider extending credit."),
                (lambda x: x < 5, "Slow", "Delayed payments", "Negotiate better payment terms.")
            ]))

        if earnings_per_share and market_price_per_share:
            pe_ratio = market_price_per_share / earnings_per_share
            results.append(analyze_ratio("P/E Ratio", pe_ratio, [
                (lambda x: x >= 15, "High", "Stock is overvalued", "Review investment risk."),
                (lambda x: x < 15, "Low", "Stock is undervalued", "Potential for growth.")
            ]))

        if dividend_per_share and market_price_per_share:
            dividend_yield = dividend_per_share / market_price_per_share
            results.append(analyze_ratio("Dividend Yield", dividend_yield, [
                (lambda x: x >= 0.03, "Attractive", "Good returns to investors", "Maintain payout."),
                (lambda x: x < 0.03, "Low", "Weak investor returns", "Consider increasing dividends.")
            ]))

        results = [r for r in results if r]
        result_df = pd.DataFrame(results)

        st.dataframe(result_df)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"results/{name.replace(' ', '_')}_{timestamp}.csv"
        result_df.to_csv(filename, index=False)

        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    result_df.to_excel(writer, index=False, sheet_name='Results')
        st.download_button(label="Download CSV", data=result_df.to_csv(index=False), file_name="financial_ratios.csv", mime="text/csv")
        st.download_button(label="Download Excel", data=buffer.getvalue(), file_name="financial_ratios.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
