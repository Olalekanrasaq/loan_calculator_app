import streamlit as st
import numpy as np
import pandas as pd


st.title('Loan Calculator')

st.write('''This loan calculator enable user to calculate the monthly/weekly/daily repayment and total interest for a loan. 
To use this app, click on the > sign at the top left corner of the app to enter the loan details. Click on calculate button after entering loan details and then click on x sign at the top to view the output loan calculations. 
''')

st.markdown("""---""")

# Sidebar
st.sidebar.title('Loan Details')
# a dropbox for selecting the loan type
loan_type = st.sidebar.selectbox('Loan Type', ['Monthly', 'Bi-weekly', 'Weekly', 'Daily'])

# input number of months if loan type is monthly
if loan_type == 'Monthly':
    loan_term = st.sidebar.number_input('Number of Months', min_value=1, value=12)

# input number of weeks if loan type is bi-weekly
if loan_type == 'Bi-weekly':
    loan_term = st.sidebar.number_input('Number of Weeks', min_value=1, value=52)

# input number of weeks if loan type is weekly
if loan_type == 'Weekly':
    loan_term = st.sidebar.number_input('Number of Weeks', min_value=1, value=52)

# input number of days if loan type is daily
if loan_type == 'Daily':
    loan_term = st.sidebar.number_input('Number of Days', min_value=1, value=365)

# input loan amount in a text format
loan_amount = st.sidebar.text_input('Loan Amount (#)', '0')

# convert the loan amount to a integer by removing thousand separator (comma) from the loan amount
loan_amount = int(loan_amount.replace(',', ''))

# input daily interest rate in a float format
daily_interest_rate = st.sidebar.number_input('Daily Interest Rate (%)', min_value=0.000, value=0.100)

# calculate the monthly interest rate
monthly_interest_rate = daily_interest_rate * 30

# calculate the weekly interest rate
weekly_interest_rate = daily_interest_rate * 7

# calculate the bi-weekly interest rate
bi_weekly_interest_rate = daily_interest_rate * 14

# processing fee
processing_fee = loan_amount * 0.001

# create a dataframe for the loan amount
def month_loan_dataframe(loan_term, loan_amount, decrease_rate, monthly_interest_rate):
    # Create a dictionary to hold the data
    data = {
        "Principal": [],
        "Interest": [],
        "Principal Repayment": [],
        "Total Repayment": []
    }

    # Populate the dictionary with values
    for month in range(loan_term):
        data["Principal"].append(round(loan_amount, 2))
        data["Interest"].append(round((loan_amount * monthly_interest_rate) / 100, 2))
        data["Principal Repayment"].append(decrease_rate)
        data["Total Repayment"].append(round((loan_amount * monthly_interest_rate) / 100 + decrease_rate, 2))
        loan_amount -= decrease_rate

    # Create a DataFrame from the dictionary and remove index
    df = pd.DataFrame(data, index=pd.Index(range(1, loan_term + 1), name="Month"))
    df.loc['Total'] = df[["Interest", "Total Repayment"]].sum()
    return df

# create a dataframe for the bi-weekly loan amount
def bi_weekly_loan_dataframe(loan_term, loan_amount, decrease_rate, bi_weekly_interest_rate):
    # Create a dictionary to hold the data
    data = {
        "Principal": [],
        "Interest": [],
        "Principal Repayment": [],
        "Total Repayment": []
    }

    # Populate the dictionary with values
    for week in range(0, loan_term, 2):
        data["Principal"].append(round(loan_amount, 2))
        data["Interest"].append(round((loan_amount * bi_weekly_interest_rate) / 100, 2))
        data["Principal Repayment"].append(decrease_rate)
        data["Total Repayment"].append(round((loan_amount * bi_weekly_interest_rate) / 100 + decrease_rate, 2))
        loan_amount -= decrease_rate

    # Create a DataFrame from the dictionary and remove index
    df = pd.DataFrame(data, index=pd.Index(range(2, loan_term + 1, 2), name="Week"))
    df.loc['Total'] = df[["Interest", "Total Repayment"]].sum()
    return df

# create a dataframe for the weekly loan amount
def weekly_loan_dataframe(loan_term, loan_amount, decrease_rate, weekly_interest_rate):
    # Create a dictionary to hold the data
    data = {
        "Principal": [],
        "Interest": [],
        "Principal Repayment": [],
        "Total Repayment": []
    }

    # Populate the dictionary with values
    for week in range(loan_term):
        data["Principal"].append(round(loan_amount, 2))
        data["Interest"].append(round((loan_amount * weekly_interest_rate) / 100, 2))
        data["Principal Repayment"].append(decrease_rate)
        data["Total Repayment"].append(round((loan_amount * weekly_interest_rate) / 100 + decrease_rate, 2))
        loan_amount -= decrease_rate

    # Create a DataFrame from the dictionary and remove index
    df = pd.DataFrame(data, index=pd.Index(range(1, loan_term + 1), name="Week"))
    df.loc['Total'] = df[["Interest", "Total Repayment"]].sum()
    return df

# create a dataframe for the daily loan amount
def daily_loan_dataframe(loan_term, loan_amount, decrease_rate, daily_interest_rate):
    # Create a dictionary to hold the data
    data = {
        "Principal": [],
        "Interest": [],
        "Principal Repayment": [],
        "Total Repayment": []
    }

    # Populate the dictionary with values
    for day in range(loan_term):
        data["Principal"].append(round(loan_amount, 2))
        data["Interest"].append(round((loan_amount * daily_interest_rate) / 100, 2))
        data["Principal Repayment"].append(decrease_rate)
        data["Total Repayment"].append(round((loan_amount * daily_interest_rate) / 100 + decrease_rate, 2))
        loan_amount -= decrease_rate

    # Create a DataFrame from the dictionary and remove index
    df = pd.DataFrame(data, index=pd.Index(range(1, loan_term + 1), name="Day"))
    df.loc['Total'] = df[["Interest", "Total Repayment"]].sum()
    return df

# input a calculate button
if st.sidebar.button('Calculate'):
    if loan_type == 'Monthly':
        st.subheader("Monthly Loan Calculations")
        st.write(f"Monthly Interest Rate: **{monthly_interest_rate:.2f}**%")
        st.write(f"Processing Fee: #**{processing_fee:,.2f}**")

        # dataframes for the loan amount
        dfs = month_loan_dataframe(loan_term, loan_amount, round(loan_amount / loan_term, 2), monthly_interest_rate)
        df = dfs.iloc[:-1]
        st.write(f"Total Interest: #**{df['Interest'].sum():,.2f}**")
        st.write(f"Total Payable: #**{(loan_amount + df['Interest'].sum()):,.2f}**")
        annual_interest_rate = (12 / loan_term) * (df['Interest'].sum() / loan_amount * 100)
        st.write(f"Effective Annual Interest Rate: **{annual_interest_rate:.2f}**%")
        eff_monthly_interest_rate = annual_interest_rate / 12
        st.write(f"Effective Monthly Interest Rate: **{eff_monthly_interest_rate:.2f}**%")
        
        st.markdown("""---""")
        st.write(dfs)

    if loan_type == 'Bi-weekly':
        st.subheader("Bi-weekly Loan Calculations")
        try:
            st.write(f"Bi-weekly Interest Rate: **{bi_weekly_interest_rate:.2f}**%")
            st.write(f"Processing Fee: #**{processing_fee:,.2f}**")
    
            # dataframes for the loan amount
            dfs = bi_weekly_loan_dataframe(loan_term, loan_amount, round(loan_amount / (loan_term*0.5), 2), bi_weekly_interest_rate)
            df = dfs.iloc[:-1]
            st.write(f"Total Interest: #**{df['Interest'].sum():,.2f}**")
            st.write(f"Total Payable: #**{(loan_amount + df['Interest'].sum()):,.2f}**")
            eff_monthly_interest_rate = (4 / loan_term) * (df['Interest'].sum() / loan_amount * 100)
            st.write(f"Effective Monthly Interest Rate (4 Weeks): **{eff_monthly_interest_rate:.2f}**%")
            eff_biweekly_interest_rate = eff_monthly_interest_rate / 2
            st.write(f"Effective Bi-weekly Interest Rate: **{eff_biweekly_interest_rate:.2f}**%")
            st.write(f"Effective Total Interest Rate: **{(df['Interest'].sum() / loan_amount * 100):.2f}**%")
            
            st.markdown("""---""")
            st.write(dfs)
        except ValueError:
            st.error("Invalid number of weeks. Bi-weekly loan accept only even number of weeks.")
    
    if loan_type == 'Weekly':
        st.subheader("Weekly Loan Calculations")
        st.write(f"7 days Interest Rate: **{weekly_interest_rate:.2f}**%")
        st.write(f"Processing Fee: #**{processing_fee:,.2f}**")

        # dataframes for the loan amount
        dfs = weekly_loan_dataframe(loan_term, loan_amount, round(loan_amount / loan_term, 2), weekly_interest_rate)
        df = dfs.iloc[:-1]
        st.write(f"Total Interest: #**{df['Interest'].sum():,.2f}**")
        st.write(f"Total Payable: #**{(loan_amount + df['Interest'].sum()):,.2f}**")
        eff_monthly_interest_rate = (4 / loan_term) * (df['Interest'].sum() / loan_amount * 100)
        st.write(f"Effective Monthly Interest Rate (4 Weeks): **{eff_monthly_interest_rate:.2f}**%")
        eff_weekly_interest_rate = eff_monthly_interest_rate / 4
        st.write(f"Effective Weekly Interest Rate: **{eff_weekly_interest_rate:.2f}**%")
        st.write(f"Effective Total Interest Rate: **{(df['Interest'].sum() / loan_amount * 100):.2f}**%")
        
        st.markdown("""---""")
        st.write(dfs)
    
    if loan_type == 'Daily':
        st.subheader("Daily Loan Calculations")
        st.write(f"Processing Fee: #**{processing_fee:,.2f}**")
        st.write(f"7 days Interest Rate: **{(daily_interest_rate*7):.2f}**%")

        # dataframes for the loan amount
        dfs = daily_loan_dataframe(loan_term, loan_amount, round(loan_amount / loan_term, 2), daily_interest_rate)
        df = dfs.iloc[:-1]
        st.write(f"Total Interest: #**{df['Interest'].sum():,.2f}**")
        st.write(f"Total Payable: #**{(loan_amount + df['Interest'].sum()):,.2f}**")
        eff_monthly_interest_rate = (4 / loan_term) * (df['Interest'].sum() / loan_amount * 100)
        st.write(f"Effective Monthly Interest Rate (4 Weeks): **{eff_monthly_interest_rate:.2f}**%")
        eff_weekly_interest_rate = eff_monthly_interest_rate / 4
        st.write(f"Effective Weekly Interest Rate: **{eff_weekly_interest_rate:.2f}**%")
        st.write(f"Effective Total Interest Rate: **{(df['Interest'].sum() / loan_amount * 100):.2f}**%")
        
        st.markdown("""---""")
        st.write(dfs)
    






