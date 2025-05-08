import streamlit as st
import pandas as pd
import csv
import os

# User and Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "adminpass"
USERS_FILE = "users.csv"

# Initialize users.csv if not exist
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["username", "status"])

# Function to check user credentials
def check_user(username):
    df = pd.read_csv(USERS_FILE)
    if username in df['username'].values:
        status = df.loc[df['username'] == username, 'status'].values[0]
        return status
    else:
        return "new"

# Function to approve users
def approve_user(username):
    df = pd.read_csv(USERS_FILE)
    df.loc[df['username'] == username, 'status'] = 'approved'
    df.to_csv(USERS_FILE, index=False)

# Session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = ""

# Login
st.title("📊 Financial Ratio Analyzer")

menu = ["Login", "Admin"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Login":
    st.subheader("User Login")
    username = st.text_input("Username")
    if st.button("Login"):
        status = check_user(username)
        if status == "approved":
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.success(f"Welcome back, {username}")
        elif status == "pending":
            st.warning("Your account is awaiting admin approval.")
        else:
            with open(USERS_FILE, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([username, "pending"])
            st.info("First time login as Free Trial. Awaiting admin approval.")

    # Show dashboard if logged in
    if st.session_state.logged_in:
        st.header(f"Financial Ratio Dashboard for {st.session_state.current_user}")

        total_assets = st.number_input("Total Assets", min_value=0.0)
        total_liabilities = st.number_input("Total Liabilities", min_value=0.0)
        inventory = st.number_input("Inventory", min_value=0.0)
        cash = st.number_input("Cash", min_value=0.0)
        operating_cf = st.number_input("Operating Cash Flow", min_value=0.0)
        investing_cf = st.number_input("Investing Cash Flow", min_value=0.0)
        financing_cf = st.number_input("Financing Cash Flow", min_value=0.0)

        if st.button("Calculate Ratios"):

            results = []

            def analyze_ratio(name, value, good_range, advice_good, advice_bad):
                analysis = "Good" if good_range[0] <= value <= good_range[1] else "Needs Attention"
                implication = "Healthy financial position." if analysis == "Good" else "Potential liquidity risk."
                advice = advice_good if analysis == "Good" else advice_bad
                return [name, round(value, 2), analysis, implication, advice]

            if total_liabilities != 0:
                current_ratio = total_assets / total_liabilities
                results.append(analyze_ratio("Current Ratio", current_ratio, (1.5, 3),
                                             "Maintain current strategy.",
                                             "Improve liquidity or reduce liabilities."))

                quick_ratio = (total_assets - inventory) / total_liabilities
                results.append(analyze_ratio("Quick Ratio", quick_ratio, (1, 2),
                                             "Strong quick assets position.",
                                             "Increase liquid assets or pay down liabilities."))

                cash_ratio = cash / total_liabilities
                results.append(analyze_ratio("Cash Ratio", cash_ratio, (0.5, 1),
                                             "Good immediate liquidity.",
                                             "Consider improving immediate cash reserves."))
            else:
                st.warning("Total Liabilities cannot be zero for ratio calculations.")

            net_cash_flow = operating_cf + investing_cf + financing_cf
            results.append(analyze_ratio("Net Cash Flow", net_cash_flow, (0, float('inf')),
                                         "Positive cash flow maintained.",
                                         "Review operational and financing activities."))

            df = pd.DataFrame(results, columns=["Ratio", "Value", "Analysis", "Implication", "Advice"])
            st.dataframe(df)

            # Save to CSV
            csv_path = "financial_ratios.csv"
            df.to_csv(csv_path, index=False)
            st.success("Results saved to financial_ratios.csv")

            # CSV download button
            with open(csv_path, "rb") as file:
                st.download_button(
                    label="📥 Download Result CSV",
                    data=file,
                    file_name="financial_ratios.csv",
                    mime="text/csv"
                )

elif choice == "Admin":
    st.subheader("Admin Panel")
    admin_user = st.text_input("Admin Username")
    admin_pass = st.text_input("Admin Password", type='password')

    if st.button("Login as Admin"):
        if admin_user == ADMIN_USERNAME and admin_pass == ADMIN_PASSWORD:
            st.success("Admin logged in.")

            df_users = pd.read_csv(USERS_FILE)
            pending_users = df_users[df_users['status'] == 'pending']

            if not pending_users.empty:
                for idx, row in pending_users.iterrows():
                    st.write(f"Username: {row['username']}")
                    if st.button(f"Approve {row['username']}"):
                        approve_user(row['username'])
                        st.success(f"{row['username']} approved.")
            else:
                st.info("No pending users.")
        else:
            st.error("Invalid admin credentials.")
