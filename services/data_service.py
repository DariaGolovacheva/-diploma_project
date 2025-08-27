# services/data_service.py
import yfinance as yf
import pandas as pd

def get_history(ticker: str, period: str = "1y") -> pd.DataFrame:
    """
    Возвращает исторические данные (DataFrame) по тикеру за period (пример: "1y", "6mo").
    """
    ticker_obj = yf.Ticker(ticker)
    hist = ticker_obj.history(period=period)
    # Убедимся, что индекс — Datetime
    if not hist.empty:
        hist = hist.reset_index()
    return hist

def get_info(ticker: str) -> dict:
    """
    Возвращает словарь с базовой info (marketCap, trailingPE и т.д.). Может быть пустым.
    """
    ticker_obj = yf.Ticker(ticker)
    try:
        info = ticker_obj.info or {}
    except Exception:
        info = {}
    return info
