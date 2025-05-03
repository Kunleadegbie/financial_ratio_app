import streamlit as st
import pandas as pd

# Input fields for financial data
st.title("Financial Ratio Analysis")

current_assets = st.number_input("Enter Current Assets", min_value=0.0, value=10000.0)
current_liabilities = st.number_input("Enter Current Liabilities", min_value=0.0, value=5000.0)
inventory = st.number_input("Enter Inventory", min_value=0.0, value=2000.0)
cash = st.number_input("Enter Cash", min_value=0.0, value=1500.0)
gross_profit = st.number_input("Enter Gross Profit", min_value=0.0, value=4000.0)
net_income = st.number_input("Enter Net Income", min_value=0.0, value=3000.0)
revenue = st.number_input("Enter Revenue", min_value=0.0, value=15000.0)
total_liabilities = st.number_input("Enter Total Liabilities", min_value=0.0, value=8000.0)
equity = st.number_input("Enter Equity", min_value=0.0, value=12000.0)
average_inventory = st.number_input("Enter Average Inventory", min_value=0.0, value=1000.0)
average_receivable = st.number_input("Enter Average Receivables", min_value=0.0, value=1200.0)
average_payable = st.number_input("Enter Average Payables", min_value=0.0, value=800.0)

# Initialize the ratios dictionary
ratios = {}

# Liquidity Ratios
if current_liabilities > 0:
    ratios["Current Ratio"] = current_assets / current_liabilities
if current_assets > 0:
    ratios["Quick Ratio"] = (current_assets - inventory) / current_liabilities
if cash > 0:
    ratios["Cash Ratio"] = cash / current_liabilities

# Profitability Ratios
if revenue > 0:
    ratios["Gross Profit Margin"] = (gross_profit / revenue) * 100
if revenue > 0:
    ratios["Net Profit Margin"] = (net_income / revenue) * 100

# Solvency Ratios
if total_liabilities > 0:
    ratios["Debt to Equity Ratio"] = total_liabilities / equity

# Efficiency Ratios
if average_inventory > 0:
    ratios["Inventory Turnover"] = gross_profit / average_inventory  # Typically, use COGS instead of gross profit
if average_receivable > 0:
    ratios["Receivables Turnover"] = revenue / average_receivable
if average_payable > 0:
    ratios["Payables Turnover"] = gross_profit / average_payable  # Typically, use COGS instead of gross profit

# Results list to store the analyzed data
results = []

# Analyze ratios
for ratio, value in ratios.items():
    if "Margin" in ratio or "%" in ratio:
        if value >= 20:
            analysis = "Strong"
            implication = "Healthy profitability"
            advice = "Maintain operational efficiency."
        elif 10 <= value < 20:
            analysis = "Average"
            implication = "Manageable but could improve"
            advice = "Review pricing and cost controls."
        else:
            analysis = "Weak"
            implication = "Profitability risk"
            advice = "Optimize revenue or reduce costs."
    else:
        if ratio == "Current Ratio":
            if value >= 2:
                analysis = "Strong"
                implication = "Good short-term liquidity"
                advice = "Maintain balance."
            elif 1 <= value < 2:
                analysis = "Weak"
                implication = "Struggle to cover short-term debts"
                advice = "Increase liquid assets."
            else:
                analysis = "Low"
                implication = "High liquidity risk"
                advice = "Improve working capital."
        elif ratio == "Quick Ratio":
            if value >= 1:
                analysis = "Strong"
                implication = "Adequate liquid assets"
                advice = "Stable financial position."
            elif 0.5 <= value < 1:
                analysis = "Weak"
                implication = "Insufficient liquid assets"
                advice = "Increase cash or receivables."
            else:
                analysis = "Low"
                implication = "Liquidity concerns"
                advice = "Boost quick assets."
        elif ratio == "Cash Ratio":
            if value >= 1:
                analysis = "Strong"
                implication = "Immediate liquidity available"
                advice = "Maintain cash reserves."
            elif 0.5 <= value < 1:
                analysis = "Weak"
                implication = "Moderate liquidity"
                advice = "Enhance cash position."
            else:
                analysis = "Low"
                implication = "Limited immediate liquidity"
                advice = "Boost cash reserves."
        else:
            analysis = "-"
            implication = "-"
            advice = "-"

    # Append results for each ratio
    results.append([ratio, round(value, 2), analysis, implication, advice])

# Create a DataFrame for displaying the results
result_df = pd.DataFrame(results, columns=["Ratio", "Value", "Analysis", "Implication", "Advice"])

# Display the results in a dataframe
st.dataframe(result_df)

# Provide a button to download the results as a CSV file
st.download_button(label="Download CSV", data=result_df.to_csv(index=False), file_name="financial_ratios.csv", mime="text/csv")
