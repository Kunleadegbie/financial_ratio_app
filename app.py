import streamlit as st
import pandas as pd
from io import BytesIO

# App title and header
st.title("📊 Financial Ratio & Cash Flow Calculator")
st.markdown("Calculate key financial ratios and cash flows based on your input figures.")

# User inputs
company = st.text_input("Company Name", "")

# Financial data inputs
revenue = st.number_input("Revenue", min_value=0.0, value=0.0)
cost_of_goods_sold = st.number_input("Cost of Goods Sold", min_value=0.0, value=0.0)
operating_profit = st.number_input("Operating Profit", min_value=0.0, value=0.0)
net_income = st.number_input("Net Income", min_value=0.0, value=0.0)
total_assets = st.number_input("Total Assets", min_value=0.0, value=0.0)
total_liabilities = st.number_input("Total Liabilities", min_value=0.0, value=0.0)
equity = st.number_input("Equity", min_value=0.0, value=0.0)
number_of_shares = st.number_input("Number of Shares Outstanding", min_value=0.0, value=0.0)

# Cash Flow data
operating_cash_flow = st.number_input("Operating Cash Flow", min_value=0.0, value=0.0)
investing_cash_flow = st.number_input("Investing Cash Flow", min_value=0.0, value=0.0)
financing_cash_flow = st.number_input("Financing Cash Flow", min_value=0.0, value=0.0)

# Button to calculate ratios
if st.button("📈 Calculate Ratios & Cash Flows"):
    # Calculate gross profit
    gross_profit = revenue - cost_of_goods_sold

    # List to hold ratio data
    ratios_data = []

    # Cash Flow figures
    ratios_data.append({
        "Ratio": "Operating Cash Flow",
        "Value": f"{operating_cash_flow:.2f}"
    })
    ratios_data.append({
        "Ratio": "Investing Cash Flow",
        "Value": f"{investing_cash_flow:.2f}"
    })
    ratios_data.append({
        "Ratio": "Financing Cash Flow",
        "Value": f"{financing_cash_flow:.2f}"
    })

    # Profitability Ratios
    if revenue != 0:
        ratios_data.append({
            "Ratio": "Gross Profit Margin",
            "Value": f"{(gross_profit / revenue) * 100:.2f}%"
        })
        ratios_data.append({
            "Ratio": "Net Profit Margin",
            "Value": f"{(net_income / revenue) * 100:.2f}%"
        })
        ratios_data.append({
            "Ratio": "Operating Profit Margin",
            "Value": f"{(operating_profit / revenue) * 100:.2f}%"
        })

    if total_assets != 0:
        ratios_data.append({
            "Ratio": "Return on Assets (ROA)",
            "Value": f"{(net_income / total_assets) * 100:.2f}%"
        })

    if equity != 0:
        ratios_data.append({
            "Ratio": "Return on Equity (ROE)",
            "Value": f"{(net_income / equity) * 100:.2f}%"
        })

    if total_liabilities != 0:
        ratios_data.append({
            "Ratio": "Debt to Equity Ratio",
            "Value": f"{(total_liabilities / equity):.2f}"
        })

    if number_of_shares != 0:
        ratios_data.append({
            "Ratio": "Earnings per Share (EPS)",
            "Value": f"{(net_income / number_of_shares):.2f}"
        })

    # Convert to DataFrame
    ratios_df = pd.DataFrame(ratios_data)

    # Display results
    st.subheader(f"📊 Financial Ratios for {company if company else 'the Company'}")
    st.dataframe(ratios_df)

    # Convert DataFrame to CSV in-memory
    csv_buffer = BytesIO()
    ratios_df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    # Download button
    st.download_button(
        label="📥 Download Ratios as CSV",
        data=csv_buffer,
        file_name=f"{company.replace(' ', '_')}_financial_ratios.csv" if company else "financial_ratios.csv",
        mime="text/csv"
    )
