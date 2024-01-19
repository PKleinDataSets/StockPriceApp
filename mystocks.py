import yfinance as yf  # Import the yfinance library for fetching stock data.
import streamlit as st  # Import the Streamlit library for creating web applications.
import pandas as pd  # Import the Pandas library for data manipulation and analysis.
import plotly.express as px  # Import Plotly Express for interactive data visualization.

# Display a heading for the web application.
st.write("""
# Simple Stock Price App

Shown are the stock **closing** price and ***volume*** of Google!
""")

# Input fields for the start and end dates to filter historical stock data.
start_date = st.date_input("Start Date", pd.to_datetime('2018-01-01'))
end_date = st.date_input("End Date", pd.to_datetime('2024-01-19'))

# Input field for the user to choose the stock symbol.
tickerSymbol = st.text_input("Enter Stock Ticker Symbol", 'GOOGL')
tickerSymbol = tickerSymbol.upper()  # Convert the input to uppercase for consistency.

# Fetch historical stock prices for the specified stock symbol and date range.
try:
    tickerData = yf.Ticker(tickerSymbol)
    tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)
except:
    st.error("Error fetching data. Please check the ticker symbol and try again.")

# Display a heading for the closing price section.
st.write('''
## Closing Price
''')

# Create an interactive line chart for the closing price using Plotly Express.
fig_close = px.line(tickerDf, x=tickerDf.index, y='Close', title='Stock Closing Price')
st.plotly_chart(fig_close)  # Display the closing price chart.

# Display a heading for the volume section.
st.write('''
## Volume
''')

# Create an interactive line chart for the volume using Plotly Express.
fig_volume = px.line(tickerDf, x=tickerDf.index, y='Volume', title='Stock Volume')
st.plotly_chart(fig_volume)  # Display the volume chart.

