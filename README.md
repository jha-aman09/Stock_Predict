# Stock Price Prediction App

## Overview

This Streamlit-based web application provides real-time stock price data visualization and prediction. It offers an intuitive interface for users to analyze stock trends and view future price predictions based on historical data.

## Features

- **Real-time Stock Data**: Fetches and displays current stock prices and key statistics.
- **Interactive Charts**: Visualize historical stock prices with adjustable time periods.
- **Price Prediction**: Utilizes an LSTM model to predict future stock prices.
- **User-friendly Interface**: Dark-themed, responsive design for enhanced user experience.
- **Multiple Time Frames**: View stock data in various time frames (1D, 5D, 1M, 6M, YTD).
- **Support for Global Stocks**: Works with US stocks and includes support for Indian stocks (NSE).

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/jha-aman09/Stock_Predict.git
   cd Stock_Predict
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Execute the application:
   ```bash
   python app.py

## Usage

1. Enter a stock symbol in the input field (e.g., AAPL for Apple Inc.).
2. View the current stock price, daily change, and key statistics.
3. Explore the interactive chart showing historical prices.
4. Select different time periods to analyze stock performance.
5. Click on "Show Price Prediction" to view future price forecasts.

## Dependencies

- Streamlit
- Plotly
- yfinance
- TensorFlow (for LSTM model)
- Pandas
- NumPy

## File Structure

- `app.py`: Main application script
- `lstm_model.py`: Implementation of the LSTM prediction model
- `requirements.txt`: List of Python dependencies

## Contributing

Contributions to improve the app are welcome. Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## Acknowledgements

- [Streamlit](https://streamlit.io/) for the web app framework
- [yfinance](https://github.com/ranaroussi/yfinance) for real-time stock data
- [Plotly](https://plotly.com/) for interactive charts

---

## Contact

Aman Jha - [LinkedIn](https://www.linkedin.com/in/aman--jha/)

Project Link: [https://github.com/jha-aman09/Stock_Predict](https://github.com/jha-aman09/Stock_Predict)
