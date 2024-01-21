import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

# Análisis Técnico
st.write('''
## Análisis Técnico
''')
# Bollinger Bands
tickerDf['Upper Band'], tickerDf['Middle Band'], tickerDf['Lower Band'] = \
    tickerDf['Close'].rolling(window=20).mean() + 2 * tickerDf['Close'].rolling(window=20).std(), \
    tickerDf['Close'].rolling(window=20).mean(), \
    tickerDf['Close'].rolling(window=20).mean() - 2 * tickerDf['Close'].rolling(window=20).std()

# Relative Strength Index (RSI)
delta = tickerDf['Close'].diff()
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)

average_gain = gain.rolling(window=14).mean()
average_loss = loss.rolling(window=14).mean()

relative_strength = average_gain / average_loss
rsi = 100 - (100 / (1 + relative_strength))

# Moving Average Convergence Divergence (MACD)
short_window = 12
long_window = 26

short_ema = tickerDf['Close'].ewm(span=short_window, adjust=False).mean()
long_ema = tickerDf['Close'].ewm(span=long_window, adjust=False).mean()

macd = short_ema - long_ema
signal_line = macd.ewm(span=9, adjust=False).mean()

# Plotting Technical Indicators
fig_tech_indicators = go.Figure()

fig_tech_indicators.add_trace(go.Scatter(x=tickerDf.index, y=tickerDf['Close'], name='Closing Price'))
fig_tech_indicators.add_trace(go.Scatter(x=tickerDf.index, y=tickerDf['Upper Band'], name='Upper Bollinger Band', line=dict(color='red', width=1.5), opacity=0.5))
fig_tech_indicators.add_trace(go.Scatter(x=tickerDf.index, y=tickerDf['Middle Band'], name='Middle Bollinger Band', line=dict(color='green', width=1.5), opacity=0.5))
fig_tech_indicators.add_trace(go.Scatter(x=tickerDf.index, y=tickerDf['Lower Band'], name='Lower Bollinger Band', line=dict(color='red', width=1.5), opacity=0.5))
fig_tech_indicators.add_trace(go.Scatter(x=tickerDf.index, y=rsi, name='RSI', line=dict(color='purple', width=1.5)))
fig_tech_indicators.add_trace(go.Bar(x=tickerDf.index, y=macd - signal_line, name='MACD Histogram', marker=dict(color='orange')))

fig_tech_indicators.update_layout(title='Technical Indicators',
                                  xaxis_rangeslider_visible=False,
                                  xaxis_title='Date',
                                  yaxis_title='Technical Indicator Values')

st.plotly_chart(fig_tech_indicators)

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

# Análisis de Rentabilidad
st.write('''
## Análisis de Rentabilidad
''')
# Calcular la rentabilidad total, considerando dividendos y posibles ajustes por divisiones de acciones
total_returns = (tickerDf['Close'].iloc[-1] / tickerDf['Close'].iloc[0]) - 1
total_returns_with_dividends = ((tickerDf['Close'].iloc[-1] + tickerDf['Dividends'].sum()) / tickerDf['Close'].iloc[0]) - 1

st.write(f"Rentabilidad total (sin considerar dividendos y divisiones): {total_returns:.2%}")
st.write(f"Rentabilidad total (considerando dividendos): {total_returns_with_dividends:.2%}")

# Personalización del Gráfico
st.write('''
## Personalización del Gráfico
''')
# Opciones para personalizar el gráfico
color_option = st.selectbox("Seleccione un color para el gráfico", ['blue', 'red', 'green', 'purple'])
title_option = st.text_input("Ingrese un título personalizado para el gráfico", f'Stock Closing Price of {tickerSymbol} Over Time')

# Crear gráfico personalizado
fig_custom = px.line(tickerDf, x=tickerDf.index, y='Close', title=title_option, labels={'Close': tickerSymbol}, line_shape='linear')
fig_custom.update_traces(line_color=color_option)

st.plotly_chart(fig_custom)

