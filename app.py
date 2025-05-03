import streamlit as st
import pandas as pd
import os
from datetime import datetime
from io import BytesIO

# Load user access CSV
USERS_CSV = "data/users.csv"

if not os.path.exists(USERS_CSV):
    df = pd.DataFrame(columns=["name", "email", "status", "trial_used"])
    df.to_csv(USERS_CSV, index=False)

users_df = pd.read_csv(USERS_CSV)

# User login inputs
st.sidebar.title("Login")
user_name = st.sidebar.text_input("Enter your Name and Surname")
user_email = st.sidebar.text_input("Enter your Email")
login_button = st.sidebar.button("Login")

def save_users_df(df):
    df.to_csv(USERS_CSV, index=False)

# Session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if login_button:
    if user_name and user_email:
        user_record = users_df[users_df['email'] == user_email]
        if user_record.empty:
            new_user = pd.DataFrame([[user_name, user_email, "pending", "no"]], columns=["name", "email", "status", "trial_used"])
            users_df = pd.concat([users_df, new_user], ignore_index=True)
            save_users_df(users_df)
            st.success("Free trial granted. Enjoy your one-time access!")
            st.session_state.logged_in = True
            users_df.loc[users_df['email'] == user_email, 'trial_used'] = 'yes'
            save_users_df(users_df)
        else:
            status = user_record.iloc[0]['status']
            trial_used = user_record.iloc[0]['trial_used']
            if status == "authorized":
                st.success("Welcome back, authorized user!")
                st.session_state.logged_in = True
            elif trial_used == "no":
                st.success("Free trial granted. Enjoy your one-time access!")
                st.session_state.logged_in = True
                users_df.loc[users_df['email'] == user_email, 'trial_used'] = 'yes'
                save_users_df(users_df)
            else:
                st.error("Access denied. Please contact admin for authorization.")
    else:
        st.warning("Please enter both Name and Email.")

# Stop if not logged in
if not st.session_state.logged_in:
    st.stop()
else:
    st.title("📊 Financial Ratio Analysis App")
    st.write(f"Hello **{user_name}** — your email: {user_email}")

    # Data inputs
    st.header("Enter Financial Figures")

    current_assets = st.number_input("Current Assets", min_value=0.0)
    current_liabilities = st.number_input("Current Liabilities", min_value=0.0)
    inventory = st.number_input("Inventory", min_value=0.0)
    cash = st.number_input("Cash & Cash Equivalents", min_value=0.0)
    gross_profit = st.number_input("Gross Profit", min_value=0.0)
    net_income = st.number_input("Net Income", min_value=0.0)
    revenue = st.number_input("Revenue", min_value=0.0)
    total_assets = st.number_input("Total Assets", min_value=0.0)
    equity = st.number_input("Equity", min_value=0.0)
    operating_profit = st.number_input("Operating Profit", min_value=0.0)
    total_liabilities = st.number_input("Total Liabilities", min_value=0.0)
    interest_expense = st.number_input("Interest Expense", min_value=0.0)

    # Calculate button
    if st.button("Calculate Ratios"):
        results = []

        # Liquidity Ratios
        current_ratio = current_assets / current_liabilities if current_liabilities else 0
        quick_ratio = (current_assets - inventory) / current_liabilities if current_liabilities else 0
        cash_ratio = cash / current_liabilities if current_liabilities else 0

        # Profitability Ratios
        gross_profit_margin = (gross_profit / revenue) * 100 if revenue else 0
        net_profit_margin = (net_income / revenue) * 100 if revenue else 0
        return_on_assets = (net_income / total_assets) * 100 if total_assets else 0
        return_on_equity = (net_income / equity) * 100 if equity else 0
        operating_margin = (operating_profit / revenue) * 100 if revenue else 0

        # Solvency Ratios
        debt_ratio = total_liabilities / total_assets if total_assets else 0
        debt_to_equity = total_liabilities / equity if equity else 0
        interest_coverage = operating_profit / interest_expense if interest_expense else 0

        # Build result DataFrame
        ratios = {
            "Current Ratio": current_ratio,
            "Quick Ratio": quick_ratio,
            "Cash Ratio": cash_ratio,
            "Gross Profit Margin (%)": gross_profit_margin,
            "Net Profit Margin (%)": net_profit_margin,
            "Return on Assets (%)": return_on_assets,
            "Return on Equity (%)": return_on_equity,
            "Operating Margin (%)": operating_margin,
            "Debt Ratio": debt_ratio,
            "Debt to Equity": debt_to_equity,
            "Interest Coverage": interest_coverage
        }

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

            results.append([ratio, round(value, 2), analysis, implication, advice])

        result_df = pd.DataFrame(results, columns=["Ratio", "Value", "Analysis", "Implication", "Advice"])

        st.dataframe(result_df)

        # Download CSV
        st.download_button(label="Download CSV", data=result_df.to_csv(index=False), file_name="financial_ratios.csv", mime="text/csv")
