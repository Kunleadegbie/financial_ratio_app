import streamlit as st
import pandas as pd
from io import BytesIO

# Set app title
st.title("📊 Financial & Banking Ratio Analysis App")

# In-memory 'database' for users and approvals
if 'users' not in st.session_state:
    st.session_state.users = {'admin': 'admin123', 'free_trial': 'trial123'}
if 'approved_users' not in st.session_state:
    st.session_state.approved_users = []

# Login form
with st.expander("🔐 Login"):
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    login_button = st.button("Login")

# Session authentication state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Login validation
if login_button:
    if username in st.session_state.users and st.session_state.users[username] == password:
        if username == "free_trial":
            if username in st.session_state.approved_users:
                st.success("Login successful as approved user.")
                st.session_state.authenticated = True
                st.session_state.current_user = username
            else:
                st.info("Free trial login successful. You need admin approval for next login.")
                st.session_state.approved_users.append(username)
                st.session_state.authenticated = True
                st.session_state.current_user = username
        else:
            st.success(f"Welcome {username}!")
            st.session_state.authenticated = True
            st.session_state.current_user = username
    else:
        st.error("Invalid username or password.")

# If authenticated, show the app
if st.session_state.authenticated:

    st.header("📑 Enter Financial Data")

    def num_input(label):
        return st.number_input(label, min_value=0.0, value=st.session_state.get(label, 0.0), key=label)

    company = st.text_input("Company Name")

    revenue = num_input("Revenue")
    cost_of_goods_sold = num_input("Cost of Goods Sold")
    operating_profit = num_input("Operating Profit")
    net_income = num_input("Net Income")
    total_assets = num_input("Total Assets")
    total_liabilities = num_input("Total Liabilities")
    equity = num_input("Equity")
    number_of_shares = num_input("Number of Shares Outstanding")
    operating_cash_flow = num_input("Operating Cash Flow")
    investing_cash_flow = num_input("Investing Cash Flow")
    financing_cash_flow = num_input("Financing Cash Flow")

    st.subheader("📌 Banking-specific Inputs")

    total_loans = num_input("Total Loans")
    total_deposits = num_input("Total Deposits")
    high_quality_liquid_assets = num_input("High-Quality Liquid Assets")
    net_cash_outflows_30d = num_input("Net Cash Outflows (30 days)")
    available_stable_funding = num_input("Available Stable Funding")
    required_stable_funding = num_input("Required Stable Funding")
    non_performing_loans = num_input("Non-Performing Loans")
    loan_loss_reserves = num_input("Loan Loss Reserves")
    net_interest_income = num_input("Net Interest Income")
    average_earning_assets = num_input("Average Earning Assets")
    operating_income = num_input("Operating Income")
    staff_costs = num_input("Staff Costs")
    tier1_capital = num_input("Tier 1 Capital")
    tier2_capital = num_input("Tier 2 Capital")
    risk_weighted_assets = num_input("Risk-Weighted Assets")
    total_assets_bank = num_input("Total Assets (for Leverage Ratio)")
    dividends = num_input("Dividends")
    net_open_position = num_input("Net Open Position (Forex Exposure)")
    capital_base = num_input("Capital Base (for Forex Exposure)")
    book_value = num_input("Book Value")

    if st.button("📈 Calculate Ratios"):
        gross_profit = revenue - cost_of_goods_sold
        data = []

        # Insight dictionary for interpretation
        insights = {
            "Gross Profit Margin": ("Measures profitability after COGS. High is better.", "Higher margin means better pricing power and cost control.", "Monitor trends to maintain healthy margins."),
            "Net Profit Margin": ("Bottom-line profitability. High is healthy.", "A high value indicates operational efficiency.", "Increase sales or reduce expenses."),
            "Operating Profit Margin": ("Profit before taxes & interest. Reflects core ops.", "Higher margins show strong core operations.", "Improve operational efficiency."),
            "Return on Assets (ROA)": ("Profit generated per asset unit.", "Higher indicates efficient asset use.", "Manage assets productively."),
            "Return on Equity (ROE)": ("Return generated on shareholders' funds.", "Higher ROE attracts investors.", "Boost profitability or manage equity."),
            "Debt to Equity Ratio": ("Measures leverage. Lower is safer.", "High ratio means greater financial risk.", "Balance debt and equity financing."),
            "Earnings per Share (EPS)": ("Profit per outstanding share.", "Higher EPS benefits shareholders.", "Focus on consistent growth."),
            "Operating Cash Flow": ("Cash generated from operations.", "Positive OCF is vital for sustainability.", "Monitor liquidity."),
            "Investing Cash Flow": ("Cash from investments.", "Negative typically means expansion.", "Ensure wise investment decisions."),
            "Financing Cash Flow": ("Cash from financing activities.", "Shows how operations are funded.", "Balance equity and debt sources."),
            "Loan-to-Deposit Ratio (LDR)": ("Shows lending aggressiveness.", "High ratio may mean liquidity strain.", "Maintain optimal LDR for stability."),
            "Liquidity Coverage Ratio (LCR)": ("Measures liquidity for 30-day stress.", "Over 100% means good resilience.", "Manage liquid asset levels."),
            "Net Stable Funding Ratio (NSFR)": ("Measures long-term funding stability.", "Over 100% ensures sustainable funding.", "Align stable funding sources."),
            "Non-Performing Loan (NPL) Ratio": ("Shows bad loans proportion.", "Lower ratio is healthier.", "Strengthen credit risk management."),
        }

        # Cash Flows
        data.append(["Operating Cash Flow", f"{operating_cash_flow:.2f}", *insights["Operating Cash Flow"]])
        data.append(["Investing Cash Flow", f"{investing_cash_flow:.2f}", *insights["Investing Cash Flow"]])
        data.append(["Financing Cash Flow", f"{financing_cash_flow:.2f}", *insights["Financing Cash Flow"]])

        # Profitability Ratios
        if revenue:
            data.append(["Gross Profit Margin", f"{(gross_profit/revenue)*100:.2f}%", *insights["Gross Profit Margin"]])
            data.append(["Net Profit Margin", f"{(net_income/revenue)*100:.2f}%", *insights["Net Profit Margin"]])
            data.append(["Operating Profit Margin", f"{(operating_profit/revenue)*100:.2f}%", *insights["Operating Profit Margin"]])

        if total_assets:
            data.append(["Return on Assets (ROA)", f"{(net_income/total_assets)*100:.2f}%", *insights["Return on Assets (ROA)"]])

        if equity:
            data.append(["Return on Equity (ROE)", f"{(net_income/equity)*100:.2f}%", *insights["Return on Equity (ROE)"]])
            data.append(["Debt to Equity Ratio", f"{(total_liabilities/equity):.2f}", *insights["Debt to Equity Ratio"]])

        if number_of_shares:
            data.append(["Earnings per Share (EPS)", f"{(net_income/number_of_shares):.2f}", *insights["Earnings per Share (EPS)"]])

        # Banking Ratios
        if total_deposits:
            data.append(["Loan-to-Deposit Ratio (LDR)", f"{(total_loans/total_deposits)*100:.2f}%", *insights["Loan-to-Deposit Ratio (LDR)"]])

        if net_cash_outflows_30d:
            data.append(["Liquidity Coverage Ratio (LCR)", f"{(high_quality_liquid_assets/net_cash_outflows_30d)*100:.2f}%", *insights["Liquidity Coverage Ratio (LCR)"]])

        if required_stable_funding:
            data.append(["Net Stable Funding Ratio (NSFR)", f"{(available_stable_funding/required_stable_funding)*100:.2f}%", *insights["Net Stable Funding Ratio (NSFR)"]])

        if total_loans:
            data.append(["Non-Performing Loan (NPL) Ratio", f"{(non_performing_loans/total_loans)*100:.2f}%", *insights["Non-Performing Loan (NPL) Ratio"]])

        # Show DataFrame
        df = pd.DataFrame(data, columns=["Ratio", "Value", "Analysis", "Implication", "Advice"])
        st.dataframe(df)

        # CSV Download
        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False)
        st.download_button("📥 Download Results as CSV", csv_buffer.getvalue(), file_name=f"{company}_Financial_Analysis.csv", mime="text/csv")

