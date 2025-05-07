import streamlit as st
import pandas as pd
import os
from io import BytesIO

USERS_CSV = "users.csv"

# Initialize users.csv if not exists or missing columns
if not os.path.exists(USERS_CSV):
    df_init = pd.DataFrame(columns=['Name', 'Email', 'Role', 'Status'])
    df_init.to_csv(USERS_CSV, index=False)
else:
    df_check = pd.read_csv(USERS_CSV)
    required_columns = ['Name', 'Email', 'Role', 'Status']
    if not all(col in df_check.columns for col in required_columns):
        df_init = pd.DataFrame(columns=required_columns)
        df_init.to_csv(USERS_CSV, index=False)

# Hardcoded admin
ADMIN_CREDENTIALS = {"name": "CHUMCRED", "email": "chumcred@gmail.com"}

st.title("📊 Financial Ratio & Cash Flow Dashboard")

st.sidebar.header("Login")
name = st.sidebar.text_input("Name")
email = st.sidebar.text_input("Email")

if st.sidebar.button("Login"):
    df_users = pd.read_csv(USERS_CSV)

    # Admin login
    if name == ADMIN_CREDENTIALS["name"] and email == ADMIN_CREDENTIALS["email"]:
        st.success("Welcome Admin!")
        st.session_state["role"] = "admin"

    else:
        user_record = df_users[(df_users['Email'] == email) & (df_users['Name'] == name)]

        if user_record.empty:
            # Free trial for new users
            new_user = pd.DataFrame([{
                "Name": name,
                "Email": email,
                "Role": "user",
                "Status": "Pending"
            }])
            df_users = pd.concat([df_users, new_user], ignore_index=True)
            df_users.to_csv(USERS_CSV, index=False)
            st.info("Free trial created. Admin approval needed for subsequent use.")
            st.session_state["role"] = "user"

        else:
            user_status = user_record.iloc[0]['Status']
            if user_status == "Pending":
                st.warning("Approval required from admin for subsequent use.")
            elif user_status == "Denied":
                st.error("Access denied by admin.")
            elif user_status == "Approved":
                st.success(f"Welcome back {name}!")
                st.session_state["role"] = "user"
            else:
                st.error("Unrecognized status. Contact admin.")

# Only show app after login
if "role" in st.session_state:

    if st.session_state["role"] == "admin":
        st.subheader("👥 User Management")
        df_users = pd.read_csv(USERS_CSV)
        st.dataframe(df_users)

        approve_email = st.text_input("User Email to Approve")
        if st.button("Approve User"):
            df_users.loc[df_users['Email'] == approve_email, 'Status'] = "Approved"
            df_users.to_csv(USERS_CSV, index=False)
            st.success(f"{approve_email} approved.")

        deny_email = st.text_input("User Email to Deny")
        if st.button("Deny User"):
            df_users.loc[df_users['Email'] == deny_email, 'Status'] = "Denied"
            df_users.to_csv(USERS_CSV, index=False)
            st.success(f"{deny_email} denied.")

    elif st.session_state["role"] == "user":
        st.header("📈 Enter Financial Data")

        # Financial Inputs
        revenue = st.number_input("Revenue", min_value=0.0, value=0.0)
        cost_of_goods_sold = st.number_input("Cost of Goods Sold", min_value=0.0, value=0.0)
        operating_profit = st.number_input("Operating Profit", min_value=0.0, value=0.0)
        net_income = st.number_input("Net Income", min_value=0.0, value=0.0)
        total_assets = st.number_input("Total Assets", min_value=0.0, value=0.0)
        total_liabilities = st.number_input("Total Liabilities", min_value=0.0, value=0.0)
        equity = st.number_input("Equity", min_value=0.0, value=0.0)
        number_of_shares = st.number_input("Number of Shares", min_value=0.0, value=0.0)

        operating_cash_flow = st.number_input("Operating Cash Flow", min_value=0.0, value=0.0)
        investing_cash_flow = st.number_input("Investing Cash Flow", min_value=0.0, value=0.0)
        financing_cash_flow = st.number_input("Financing Cash Flow", min_value=0.0, value=0.0)

        total_loans = st.number_input("Total Loans", min_value=0.0, value=0.0)
        total_deposits = st.number_input("Total Deposits", min_value=0.0, value=0.0)
        non_performing_loans = st.number_input("Non-Performing Loans", min_value=0.0, value=0.0)

        if st.button("Calculate Ratios"):
            ratios = []

            # Financial Ratio Calculations (from original opp.py structure)
            try:
                gross_profit_margin = (revenue - cost_of_goods_sold) / revenue * 100 if revenue else 0
                net_profit_margin = (net_income / revenue) * 100 if revenue else 0
                roa = (net_income / total_assets) * 100 if total_assets else 0
                roe = (net_income / equity) * 100 if equity else 0
                debt_equity_ratio = (total_liabilities / equity) if equity else 0
                earnings_per_share = (net_income / number_of_shares) if number_of_shares else 0
                cash_flow_ratio = (operating_cash_flow / total_liabilities) if total_liabilities else 0
                npl_ratio = (non_performing_loans / total_loans) * 100 if total_loans else 0

                ratios.append(["Gross Profit Margin", f"{gross_profit_margin:.2f}%", "Profitability after cost of sales", "Higher is better", "Increase sales, reduce cost"])
                ratios.append(["Net Profit Margin", f"{net_profit_margin:.2f}%", "Profitability after all expenses", "Higher is better", "Improve efficiency"])
                ratios.append(["Return on Assets (ROA)", f"{roa:.2f}%", "Return per unit of assets", "Higher is better", "Optimize asset usage"])
                ratios.append(["Return on Equity (ROE)", f"{roe:.2f}%", "Return on shareholders' funds", "Higher is better", "Boost profitability"])
                ratios.append(["Debt to Equity Ratio", f"{debt_equity_ratio:.2f}", "Leverage indicator", "Lower is safer", "Reduce debt exposure"])
                ratios.append(["Earnings Per Share (EPS)", f"{earnings_per_share:.2f}", "Profit per share", "Higher attracts investors", "Grow profits"])
                ratios.append(["Cash Flow Ratio", f"{cash_flow_ratio:.2f}", "Liquidity indicator", "Higher is better", "Improve cash inflow"])
                ratios.append(["Non-Performing Loan (NPL) Ratio", f"{npl_ratio:.2f}%", "Loan quality indicator", "Lower is better", "Manage credit risk"])

                df_ratios = pd.DataFrame(ratios, columns=["Ratio", "Value", "Analysis", "Implication", "Advice"])
                st.subheader("📑 Financial Ratios Summary")
                st.dataframe(df_ratios)

                # CSV download button
                csv = df_ratios.to_csv(index=False).encode()
                st.download_button("📥 Download Ratios CSV", data=csv, file_name="financial_ratios.csv", mime="text/csv")

            except Exception as e:
                st.error(f"Error during calculation: {e}")
