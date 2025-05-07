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
            try:
                ratios = []
                gross_profit = revenue - cost_of_goods_sold

                ratios.append({"Ratio": "Gross Profit Margin", "Value": f"{(gross_profit / revenue) * 100:.2f}%" if revenue else "N/A", "Analysis": "Profitability after direct costs", "Implication": "Higher is better", "Advice": "Control costs."})
                ratios.append({"Ratio": "Net Profit Margin", "Value": f"{(net_income / revenue) * 100:.2f}%" if revenue else "N/A", "Analysis": "Overall profitability", "Implication": "Higher is better", "Advice": "Increase revenue, cut costs."})
                ratios.append({"Ratio": "Operating Profit Margin", "Value": f"{(operating_profit / revenue) * 100:.2f}%" if revenue else "N/A", "Analysis": "Profit from operations", "Implication": "Higher is better", "Advice": "Boost operations."})

                ratios.append({"Ratio": "Return on Assets (ROA)", "Value": f"{(net_income / total_assets) * 100:.2f}%" if total_assets else "N/A", "Analysis": "Efficiency of asset use", "Implication": "Higher is better", "Advice": "Optimize assets."})
                ratios.append({"Ratio": "Return on Equity (ROE)", "Value": f"{(net_income / equity) * 100:.2f}%" if equity else "N/A", "Analysis": "Return to shareholders", "Implication": "Higher is better", "Advice": "Grow net income."})
                ratios.append({"Ratio": "Debt-to-Equity", "Value": f"{(total_liabilities / equity):.2f}" if equity else "N/A", "Analysis": "Leverage position", "Implication": "Lower is safer", "Advice": "Manage debt levels."})
                ratios.append({"Ratio": "Earnings per Share (EPS)", "Value": f"{(net_income / number_of_shares):.2f}" if number_of_shares else "N/A", "Analysis": "Shareholder return", "Implication": "Higher is better", "Advice": "Improve earnings."})

                # Banking ratios
                ldr = (total_loans / total_deposits) if total_deposits else 0.0
                npl = (non_performing_loans / total_loans) if total_loans else 0.0
                ratios.append({"Ratio": "Loan-to-Deposit Ratio (LDR)", "Value": f"{ldr:.2%}", "Analysis": "Loan funding coverage", "Implication": "Too high is risky", "Advice": "Balance deposits and loans."})
                ratios.append({"Ratio": "Non-Performing Loans (NPL) Ratio", "Value": f"{npl:.2%}", "Analysis": "Loan portfolio health", "Implication": "Lower is better", "Advice": "Reduce bad loans."})

                # Cash Flows
                ratios.append({"Ratio": "Operating Cash Flow", "Value": f"{operating_cash_flow:,.2f}", "Analysis": "Liquidity from operations", "Implication": "Positive is healthy", "Advice": "Boost cash flows."})
                ratios.append({"Ratio": "Investing Cash Flow", "Value": f"{investing_cash_flow:,.2f}", "Analysis": "Investments", "Implication": "Negative is normal", "Advice": "Invest wisely."})
                ratios.append({"Ratio": "Financing Cash Flow", "Value": f"{financing_cash_flow:,.2f}", "Analysis": "Funding activities", "Implication": "Context dependent", "Advice": "Balance funding needs."})

                df_result = pd.DataFrame(ratios)
                st.subheader("📊 Results")
                st.dataframe(df_result)

                # CSV Download
                csv_buffer = BytesIO()
                df_result.to_csv(csv_buffer, index=False)
                csv_buffer.seek(0)

                st.download_button(
                    label="📥 Download as CSV",
                    data=csv_buffer,
                    file_name="financial_ratios.csv",
                    mime="text/csv"
                )

            except Exception as e:
                st.error(f"Calculation error: {e}")
