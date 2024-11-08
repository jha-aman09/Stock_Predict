import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
import yfinance as yf
from lstm_model import prepare_stock_data

# Set dark theme
st.set_page_config(
    page_title="Stock Price Prediction",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme
st.markdown("""
    <style>
    .stApp {
        background-color: #202124;
        color: #ffffff;
    }
    .stock-header {
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 0.5em;
    }
    .stock-price {
        font-size: 2em;
        font-weight: bold;
    }
    .price-change {
        color: #ff4444;
        font-size: 1.2em;
    }
    .metric-card {
        background-color: #303134;
        padding: 1em;
        border-radius: 10px;
        margin: 0.5em;
    }
    .tab-container {
        display: flex;
        gap: 1em;
        margin-bottom: 1em;
    }
    .tab {
        background-color: #303134;
        padding: 0.5em 2em;
        border-radius: 20px;
        cursor: pointer;
    }
    .tab.active {
        background-color: #8ab4f8;
        color: #202124;
    }
    </style>
    """, unsafe_allow_html=True)

st.title('Stock Price Prediction App')

# Input for stock symbol
symbol = st.text_input("Enter Stock Symbol (e.g., AAPL, MSFT, AMZN):")

# Common stock symbols
common_symbols = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'FB', 'TSLA', 'NVDA', 'JPM', 'JNJ', 'V']

if symbol:
    try:
        # Check if the symbol needs a suffix
        if '.' not in symbol and symbol.isalpha():
            symbol = f"{symbol}"  # Add .NS suffix for Indian stocks
        
        # Fetch current stock data
        stock = yf.Ticker(symbol)
        current_data = stock.history(period='1d')
        
        if current_data.empty:
            st.error(f"No data found for symbol {symbol}. Please check the symbol and try again.")
            st.info(f"Here are some common stock symbols you can try: {', '.join(common_symbols)}")
        else:
            current_price = current_data['Close'].iloc[-1]
            price_change = current_data['Close'].iloc[-1] - current_data['Open'].iloc[0]
            price_change_percent = (price_change / current_data['Open'].iloc[0]) * 100
            
            # Display stock header and current price
            st.markdown(f"<div class='stock-header'>{stock.info.get('longName', symbol)}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='stock-price'>{current_price:.2f} {stock.info.get('currency', 'USD')}</div>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='price-change'>{price_change:.2f} ({price_change_percent:.2f}%) today</div>",
                unsafe_allow_html=True
            )

            # Time period selector
            periods = ['1D', '5D', '1M', '6M', 'YTD', 'More']
            selected_period = st.select_slider('Select Time Period', options=periods, value='1D')

            # Fetch and display stock data based on selected period
            if selected_period == '1D':
                historical_data = stock.history(interval='5m', period='1d')
            elif selected_period == '5D':
                historical_data = stock.history(interval='15m', period='5d')
            elif selected_period == '1M':
                historical_data = stock.history(interval='1d', period='1mo')
            elif selected_period == '6M':
                historical_data = stock.history(interval='1d', period='6mo')
            else:
                historical_data = stock.history(interval='1d', period='ytd')

            # Create price chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=historical_data.index,
                y=historical_data['Close'],
                mode='lines',
                name='Price',
                line=dict(color='#8ab4f8')
            ))

            fig.update_layout(
                plot_bgcolor='#202124',
                paper_bgcolor='#202124',
                font=dict(color='#ffffff'),
                margin=dict(l=0, r=0, t=0, b=0),
                yaxis=dict(
                    gridcolor='#303134',
                    zerolinecolor='#303134',
                ),
                xaxis=dict(
                    gridcolor='#303134',
                    zerolinecolor='#303134',
                )
            )

            st.plotly_chart(fig, use_container_width=True)

            # Display key statistics in a grid
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("""
                    <div class='metric-card'>
                        <div>Open</div>
                        <div style='font-size: 1.2em; font-weight: bold;'>
                            {:.2f}
                        </div>
                    </div>
                """.format(current_data['Open'].iloc[0]), unsafe_allow_html=True)
                
            with col2:
                st.markdown("""
                    <div class='metric-card'>
                        <div>High</div>
                        <div style='font-size: 1.2em; font-weight: bold;'>
                            {:.2f}
                        </div>
                    </div>
                """.format(current_data['High'].iloc[0]), unsafe_allow_html=True)
                
            with col3:
                st.markdown("""
                    <div class='metric-card'>
                        <div>Low</div>
                        <div style='font-size: 1.2em; font-weight: bold;'>
                            {:.2f}
                        </div>
                    </div>
                """.format(current_data['Low'].iloc[0]), unsafe_allow_html=True)
                
            with col4:
                st.markdown("""
                    <div class='metric-card'>
                        <div>P/E Ratio</div>
                        <div style='font-size: 1.2em; font-weight: bold;'>
                            {:.2f}
                        </div>
                    </div>
                """.format(stock.info.get('trailingPE', 0)), unsafe_allow_html=True)

            # Add prediction button
            if st.button("Show Price Prediction"):
                with st.spinner("Generating price prediction..."):
                    try:
                        historical_data, future_data = prepare_stock_data(symbol)
                        
                        # Display future prediction chart
                        fig_future = go.Figure()
                        fig_future.add_trace(go.Scatter(
                            x=future_data['Date'][:15],
                            y=future_data['Predicted_Close'][:15],
                            mode='lines+markers',
                            name='Predicted Price',
                            line=dict(color='#8ab4f8')
                        ))

                        fig_future.update_layout(
                            title="15-Day Price Prediction",
                            plot_bgcolor='#202124',
                            paper_bgcolor='#202124',
                            font=dict(color='#ffffff'),
                            margin=dict(l=0, r=0, t=30, b=0),
                            yaxis=dict(
                                gridcolor='#303134',
                                zerolinecolor='#303134',
                            ),
                            xaxis=dict(
                                gridcolor='#303134',
                                zerolinecolor='#303134',
                            )
                        )

                        st.plotly_chart(fig_future, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error generating prediction: {str(e)}")
                        st.info("This could be due to insufficient historical data or an issue with the prediction model.")

    except Exception as e:
        st.error(f"Error fetching data for {symbol}. Please check the symbol and try again.")
        st.info(f"Here are some common stock symbols you can try: {', '.join(common_symbols)}")
        st.error(f"Detailed error: {str(e)}")

st.markdown("Note: For Indian stocks, add '.NS' to the symbol (e.g., HDFCBANK.NS)")