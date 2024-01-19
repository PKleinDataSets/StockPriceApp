import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.express as px

st.write("""
# Simple Stock Price App

Shown are the stock **closing** price and ***volume*** of Google!

""")

# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75
#define the ticker symbol

# input the start date and de end date

start_date = st.date_input("Start Date", pd.to_datetime('2010-05-31'))
end_date = st.date_input("End Date", pd.to_datetime('2020-05-31'))

# the user choose the simbol of the stock
#get data on this ticker
tickerSymbol = st.text_input("Enter Stock Ticker Symbol", 'GOOGL')
tickerSymbol = tickerSymbol.upper()

#get the historical prices for this ticker
try:
    tickerData = yf.Ticker(tickerSymbol)
    tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)
except:
    st.error("Error fetching data. Please check the ticker symbol and try again.")

# Open	High	Low	Close	Volume	Dividends	Stock Splits

st.write('''
##Closing Price
''')
# st.line_chart(tickerDf.Close)
fig_close = px.line(tickerDf, x=tickerDf.index, y='Close', title='Stock Closing Price')
st.plotly_chart(fig_close)

st.write('''
##Volumen
''')
#st.line_chart(tickerDf.Volume)
fig_volume = px.line(tickerDf, x=tickerDf.index, y='Volume', title='Stock Volume')
st.plotly_chart(fig_volume)

