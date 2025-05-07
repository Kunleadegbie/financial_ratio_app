import streamlit as st
import pandas as pd
from io import BytesIO
import os

# Define CSV file for users
USERS_CSV = 'users.csv'

# Predefined admin credentials
ADMIN_EMAIL = 'seedtimecapital@gmail.com'
ADMIN_PASSWORD = 'admin1234'

# Initialize users CSV if not exists
if not os.path.exists(USERS_CSV):
    df_init = pd.DataFrame(columns=['Name', 'Email', 'Role', 'Approval'])
    df_init.to_csv(USERS_CSV, index=False)

# Load users
df_users = pd.read_csv(USERS_CSV)

# Sidebar login
st.sidebar.title('Login')
name = st.sidebar.text_input('Name')
email = st.sidebar.text_input('Email')
password = st.sidebar.text_input('Password', type='password')

if st.sidebar.button('Login'):
    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
        st.sidebar.success('Logged in as Admin')
        role = 'Admin'
    else:
        user_record = df_users[(df_users['Email'] == email) & (df_users['Name'] == name)]
        if user_record.empty:
            new_user = pd.DataFrame([{'Name': name, 'Email': email, 'Role': 'User', 'Approval': 'Pending'}])
            df_users = pd.concat([df_users, new_user], ignore_index=True)
            df_users.to_csv(USERS_CSV, index=False)
            st.sidebar.info('Free trial activated, awaiting admin approval for next login.')
            st.stop()
        else:
            approval_status = user_record.iloc[0]['Approval']
            if approval_status == 'Approved':
                st.sidebar.success(f'Welcome {name}')
                role = 'User'
            elif approval_status == 'Denied':
                st.sidebar.error('Access Denied by Admin.')
                st.stop()
            else:
                st.sidebar.warning('Approval pending. Contact Admin.')
                st.stop()

    st.title("📊 Financial Ratio & Cash Flow Calculator (Bank Edition)")

    company = st.text_input("Company Name")

    st.header("General Financial Data")
    revenue = st.number_input("Revenue", min_value=0.0)
    cost_of_goods_sold = st.number_input("Cost of Goods Sold", min_value=0.0)
    operating_profit = st.number_input("Operating Profit", min_value=0.0)
    net_income = st.number_input("Net Income", min_value=0.0)
    total_assets = st.number_input("Total Assets", min_value=0.0)
    total_liabilities = st.number_input("Total Liabilities", min_value=0.0)
    equity = st.number_input("Equity", min_value=0.0)
    number_of_shares = st.number_input("Number of Shares Outstanding", min_value=0.0)

    st.header("Cash Flow Data")
    operating_cash_flow = st.number_input("Operating Cash Flow", min_value=0.0)
    investing_cash_flow = st.number_input("Investing Cash Flow", min_value=0.0)
    financing_cash_flow = st.number_input("Financing Cash Flow", min_value=0.0)

    st.header("Banking Financial Data")
    total_loans = st.number_input("Total Loans", min_value=0.0)
    total_deposits = st.number_input("Total Deposits", min_value=0.0)
    non_performing_loans = st.number_input("Non-Performing Loans", min_value=0.0)

    if st.button("📈 Calculate Ratios & Cash Flows"):
        gross_profit = revenue - cost_of_goods_sold
        ratios_data = []

        ratios_data.append({"Ratio": "Operating Cash Flow", "Value": f"{operating_cash_flow:,.2f}"})
        ratios_data.append({"Ratio": "Investing Cash Flow", "Value": f"{investing_cash_flow:,.2f}"})
        ratios_data.append({"Ratio": "Financing Cash Flow", "Value": f"{financing_cash_flow:,.2f}"})

        if revenue != 0:
            ratios_data.append({"Ratio": "Gross Profit Margin", "Value": f"{(gross_profit / revenue) * 100:.2f}%"})
            ratios_data.append({"Ratio": "Net Profit Margin", "Value": f"{(net_income / revenue) * 100:.2f}%"})
            ratios_data.append({"Ratio": "Operating Profit Margin", "Value": f"{(operating_profit / revenue) * 100:.2f}%"})

        if total_assets != 0:
            ratios_data.append({"Ratio": "Return on Assets (ROA)", "Value": f"{(net_income / total_assets) * 100:.2f}%"})

        if equity != 0:
            ratios_data.append({"Ratio": "Return on Equity (ROE)", "Value": f"{(net_income / equity) * 100:.2f}%"})
            ratios_data.append({"Ratio": "Debt to Equity Ratio", "Value": f"{(total_liabilities / equity):.2f}"})

        if number_of_shares != 0:
            ratios_data.append({"Ratio": "Earnings per Share (EPS)", "Value": f"{(net_income / number_of_shares):.2f}"})

        ldr = (total_loans / total_deposits) if total_deposits != 0 else 0.0
        ratios_data.append({"Ratio": "Loan-to-Deposit Ratio (LDR)", "Value": f"{ldr:.2%}"})

        npl_ratio = (non_performing_loans / total_loans) if total_loans != 0 else 0.0
        ratios_data.append({"Ratio": "Non-Performing Loan (NPL) Ratio", "Value": f"{npl_ratio:.2%}"})

        ratios_df = pd.DataFrame(ratios_data)
        st.subheader(f"📊 Financial Ratios for {company if company else 'the Company'}")
        st.dataframe(ratios_df)

        csv_buffer = BytesIO()
        ratios_df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)

        st.download_button(
            label="📥 Download Ratios as CSV",
            data=csv_buffer,
            file_name=f"{company.replace(' ', '_')}_financial_ratios.csv" if company else "financial_ratios.csv",
            mime="text/csv"
        )
