import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.express as px

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

# Media Móvil
st.write('''
## Media Móvil
''')
# Input para el período de la media móvil
ma_period = st.slider("Seleccionar período de Media Móvil", min_value=1, max_value=100, value=20)

# Calcular la media móvil de los precios de cierre
tickerDf['Close_MA'] = tickerDf['Close'].rolling(window=ma_period).mean()

# Crear gráfico con la media móvil
fig_ma = px.line(tickerDf, x=tickerDf.index, y=['Close', 'Close_MA'], title=f'Stock Closing Price with {ma_period}-Day Moving Average')
st.plotly_chart(fig_ma)

# Display a heading for the volume section.
st.write('''
## Volume
''')

# Create an interactive line chart for the volume using Plotly Express.
fig_volume = px.line(tickerDf, x=tickerDf.index, y='Volume', title='Stock Volume')
st.plotly_chart(fig_volume)  # Display the volume chart.

# Comparación de Acciones
st.write('''
## Comparación de Acciones
''')
# Input para agregar múltiples acciones
multiple_tickers = st.text_area("Agregar múltiples acciones (separadas por comas)", 'AAPL, MSFT, AMZN')
multiple_tickers = [ticker.strip().upper() for ticker in multiple_tickers.split(',')]

# Obtener datos históricos para las acciones adicionales
try:
    multiple_ticker_data = {ticker: yf.Ticker(ticker).history(period='1d', start=start_date, end=end_date) for ticker in multiple_tickers}
except:
    st.error("Error fetching data for additional tickers. Please check the ticker symbols and try again.")

# Crear gráfico comparativo de precios de cierre
fig_comparison_close = px.line(tickerDf, x=tickerDf.index, y='Close', title='Stock Closing Price Comparison', labels={'Close': tickerSymbol})
for ticker, data in multiple_ticker_data.items():
    fig_comparison_close.add_scatter(x=data.index, y=data['Close'], mode='lines', name=ticker)

st.plotly_chart(fig_comparison_close)

# Estadísticas Descriptivas
st.write('''
## Estadísticas Descriptivas
''')
# Calcular estadísticas descriptivas
descriptive_stats = tickerDf[['Close', 'Volume']].describe()

# Mostrar las estadísticas descriptivas
st.write(descriptive_stats)
