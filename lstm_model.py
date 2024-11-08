import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from datetime import datetime, timedelta

def fetch_stock_data(symbol, start_date, end_date):
    stock = yf.Ticker(symbol)
    df = stock.history(start=start_date, end=end_date)
    return df[['Open', 'High', 'Low', 'Close', 'Volume']]

def create_lstm_model(data, time_steps, future_days):
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)

    X, y = [], []
    for i in range(time_steps, len(scaled_data) - future_days + 1):
        X.append(scaled_data[i-time_steps:i])
        y.append(scaled_data[i:i+future_days, 3])  # Predicting 'Close' price

    X, y = np.array(X), np.array(y)

    # Get the number of features (should be 5: Open, High, Low, Close, Volume)
    n_features = X.shape[2]

    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(time_steps, n_features)),
        LSTM(50, return_sequences=False),
        Dense(future_days)
    ])

    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=50, batch_size=32, validation_split=0.1, verbose=1)

    return model, scaler

def predict_future_prices(model, scaler, last_sequence, future_days):
    last_sequence_scaled = scaler.transform(last_sequence)
    predicted_scaled = model.predict(np.array([last_sequence_scaled]))
    predicted = scaler.inverse_transform(np.column_stack((predicted_scaled[0], np.zeros((future_days, 4)))))
    return predicted[:, 0]

def prepare_stock_data(symbol):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365*5)  # Using 5 years of data
    data = fetch_stock_data(symbol, start_date, end_date)
    
    time_steps = 60
    future_days = 15  # Changed to 15 days as per the chart

    model, scaler = create_lstm_model(data, time_steps, future_days)
    
    last_sequence = data.iloc[-time_steps:].values
    future_prices = predict_future_prices(model, scaler, last_sequence, future_days)

    future_dates = pd.date_range(start=end_date, periods=future_days)
    future_df = pd.DataFrame({'Date': future_dates, 'Predicted_Close': future_prices})

    return data, future_df

if __name__ == "__main__":
    # Test the model
    symbol = "AAPL"
    historical_data, future_data = prepare_stock_data(symbol)
    print(f"Historical data shape: {historical_data.shape}")
    print(f"Future data shape: {future_data.shape}")