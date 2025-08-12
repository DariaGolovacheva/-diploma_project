import yfinance as yf
import pandas as pd

def get_stock_data(ticker, period="1y"):
    data = yf.download(ticker, period=period)
    data.reset_index(inplace=True)
    return data

if __name__ == "__main__":
    df = get_stock_data("AAPL")
    print(df.head())
