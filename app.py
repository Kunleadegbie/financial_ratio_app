import streamlit as st
import pandas as pd
from io import StringIO

# User database file (persistent storage for users)
users_file = 'users.csv'

# Check if users file exists, if not, create one
def check_and_create_users_file():
    try:
        users_df = pd.read_csv(users_file)
    except FileNotFoundError:
        users_df = pd.DataFrame(columns=["email", "name", "role"])
        users_df.to_csv(users_file, index=False)

# Function to check if the user is an admin (can modify this logic)
def is_admin(email):
    return email == "admin@example.com"

# Function to capture new user
def capture_user(email, name):
    user = {"email": email, "name": name, "role": "Admin" if is_admin(email) else "Regular"}
    users_df = pd.read_csv(users_file)

    # Convert user dict to DataFrame for concatenation
    new_user_df = pd.DataFrame([user])

    # Concatenate the new user DataFrame to the existing one
    users_df = pd.concat([users_df, new_user_df], ignore_index=True)

    # Save back to CSV
    users_df.to_csv(users_file, index=False)

# Function to display all users (admin only)
def display_users():
    users_df = pd.read_csv(users_file)
    st.subheader("All Users")
    st.write(users_df)

# Function to calculate financial ratios
def calculate_financial_ratios():
    # User input for financial figures
    current_assets = st.number_input("Enter Current Assets", min_value=0.0)
    current_liabilities = st.number_input("Enter Current Liabilities", min_value=0.0)
    cash_and_equivalents = st.number_input("Enter Cash and Cash Equivalents", min_value=0.0)
    total_debt = st.number_input("Enter Total Debt", min_value=0.0)
    total_equity = st.number_input("Enter Total Equity", min_value=0.0)
    gross_profit = st.number_input("Enter Gross Profit", min_value=0.0)
    total_assets = st.number_input("Enter Total Assets", min_value=0.0)
    net_income = st.number_input("Enter Net Income", min_value=0.0)
    earnings_shares = st.number_input("Enter Earnings per Share", min_value=0.0)
    cash_flow = st.number_input("Enter Net Cash Flow", min_value=0.0)

    # Calculations
    current_ratio = current_assets / current_liabilities if current_liabilities != 0 else 0
    quick_ratio = (current_assets - cash_and_equivalents) / current_liabilities if current_liabilities != 0 else 0
    cash_ratio = cash_and_equivalents / current_liabilities if current_liabilities != 0 else 0
    debt_to_equity = total_debt / total_equity if total_equity != 0 else 0
    gross_profit_margin = gross_profit / total_assets if total_assets != 0 else 0
    return_on_assets = net_income / total_assets if total_assets != 0 else 0
    return_on_equity = net_income / total_equity if total_equity != 0 else 0
    earnings_per_share = net_income / earnings_shares if earnings_shares != 0 else 0
    net_cash_flow = cash_flow

    # Financial ratios and analysis
    ratios_data = [
        {"Ratio": "Current Ratio", "Value": f"{current_ratio:.2f}",
         "Analysis": "Weak" if current_ratio < 1 else "Good", "Implication": "Struggle to cover short-term debts" if current_ratio < 1 else "Healthy short-term liquidity",
         "Advice": "Increase liquid assets." if current_ratio < 1 else "Maintain current liquidity."},

        {"Ratio": "Quick Ratio", "Value": f"{quick_ratio:.2f}",
         "Analysis": "Weak" if quick_ratio < 1 else "Good", "Implication": "Insufficient liquid assets" if quick_ratio < 1 else "Sufficient liquid assets",
         "Advice": "Increase cash or receivables." if quick_ratio < 1 else "Maintain liquid assets."},

        {"Ratio": "Cash Ratio", "Value": f"{cash_ratio:.2f}",
         "Analysis": "Low" if cash_ratio < 0.5 else "Good", "Implication": "Limited immediate liquidity" if cash_ratio < 0.5 else "Strong immediate liquidity",
         "Advice": "Boost cash reserves." if cash_ratio < 0.5 else "Maintain strong liquidity."},

        {"Ratio": "Debt-to-Equity", "Value": f"{debt_to_equity:.2f}",
         "Analysis": "Healthy" if debt_to_equity < 1 else "High", "Implication": "Balanced capital structure" if debt_to_equity < 1 else "High leverage",
         "Advice": "Maintain leverage." if debt_to_equity < 1 else "Consider reducing debt."},

        {"Ratio": "Gross Profit Margin", "Value": f"{gross_profit_margin:.2f}",
         "Analysis": "Good" if gross_profit_margin > 0.4 else "Weak", "Implication": "Healthy profit margin" if gross_profit_margin > 0.4 else "Low margin",
         "Advice": "Maintain margins." if gross_profit_margin > 0.4 else "Improve profit margins."},

        {"Ratio": "Return on Assets (ROA)", "Value": f"{return_on_assets:.2f}",
         "Analysis": "Good" if return_on_assets > 0.1 else "Weak", "Implication": "Efficient asset utilization" if return_on_assets > 0.1 else "Low efficiency",
         "Advice": "Maintain efficiency." if return_on_assets > 0.1 else "Improve asset utilization."},

        {"Ratio": "Return on Equity (ROE)", "Value": f"{return_on_equity:.2f}",
         "Analysis": "Strong" if return_on_equity > 0.2 else "Weak", "Implication": "Good shareholder returns" if return_on_equity > 0.2 else "Low returns",
         "Advice": "Maintain profitability." if return_on_equity > 0.2 else "Focus on profitability."},

        {"Ratio": "Earnings Per Share (EPS)", "Value": f"{earnings_per_share:.2f}",
         "Analysis": "Low" if earnings_per_share < 1 else "Good", "Implication": "Low profitability per share" if earnings_per_share < 1 else "Healthy earnings per share",
         "Advice": "Grow net income or reduce share dilution." if earnings_per_share < 1 else "Maintain or improve EPS."},

        {"Ratio": "Net Cash Flow", "Value": f"{net_cash_flow:.2f}",
         "Analysis": "Negative" if net_cash_flow < 0 else "Positive", "Implication": "Potential liquidity issues" if net_cash_flow < 0 else "Strong cash generation",
         "Advice": "Consider cost reduction or increasing revenue." if net_cash_flow < 0 else "Maintain or improve positive cash flow."}
    ]

    # Convert to DataFrame for CSV download
    df = pd.DataFrame(ratios_data)

    # Convert DataFrame to CSV
    csv = df.to_csv(index=False)

    # Create a downloadable link for CSV
    st.download_button(
        label="Download Financial Ratios CSV",
        data=csv,
        file_name="financial_ratios.csv",
        mime="text/csv"
    )

    # Display ratios and analysis on the app
    for ratio in ratios_data:
        st.write(f"**{ratio['Ratio']}**: {ratio['Value']}")
        st.write(f"**Analysis**: {ratio['Analysis']}")
        st.write(f"**Implication**: {ratio['Implication']}")
        st.write(f"**Advice**: {ratio['Advice']}")
        st.markdown("---")

# Streamlit app
if __name__ == "__main__":
    st.title("Financial Ratio Calculator")
    st.sidebar.header("Enter Your Details")
    
    # Initialize the user file if it doesn't exist
    check_and_create_users_file()

    # User login
    st.sidebar.subheader("Login")
    user_name = st.sidebar.text_input("Name")
    user_email = st.sidebar.text_input("Email")

    if st.sidebar.button("Login"):
        if user_name and user_email:
            # Capture the user data
            capture_user(user_email, user_name)

            # Greet user
            st.sidebar.success(f"Welcome {user_name}!")

            # If user is an admin, allow viewing of all users
            if is_admin(user_email):
                display_users()

            # Proceed with the financial ratio calculation
            calculate_financial_ratios()
        else:
            st.sidebar.error("Please enter both name and email to log in.")

