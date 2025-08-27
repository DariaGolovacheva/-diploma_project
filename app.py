from flask import Flask, render_template, request
import yfinance as yf

from services.data_service import get_history, get_info
from services.plotting import plot_price
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/company", methods=["GET", "POST"])
def company():
    if request.method == "POST":
        ticker = request.form.get("ticker")
        if ticker:
            try:
                data = yf.download(ticker, period="6mo")
                if data.empty:
                    return f"Нет данных по тикеру {ticker}.", 404
                table_html = data.tail(10).to_html(classes="table table-striped")
                return render_template("company.html", ticker=ticker, table_html=table_html)
            except Exception as e:
                return f"Ошибка: {str(e)}", 500
        else:
            return "Введите тикер компании.", 400
    return render_template("company_form.html")



@app.route("/dashboard/<ticker>", methods=["GET"])
def dashboard(ticker):
    ticker = ticker.upper()
    # 1) Получаем историю цен (1 год)
    history = get_history(ticker, period="1y")
    # 2) Строим и сохраняем график (возвращает относительный путь)
    plot_url = plot_price(history, ticker, app.root_path)

    # 3) Получаем info с основными показателями (marketCap, trailingPE, debtToEquity может быть)
    info = get_info(ticker)

    # Подготовим метрики для отображения (защитимся от отсутствия данных)
    def fmt(val):
        try:
            if val is None:
                return "N/A"
            # большие числа
            if isinstance(val, (int, float)) and abs(val) >= 1e6:
                return f"{val:,.0f}"
            return str(val)
        except Exception:
            return "N/A"

    metrics = {
        "Market Cap": fmt(info.get("marketCap")),
        "Trailing P/E": fmt(info.get("trailingPE")),
        "Forward P/E": fmt(info.get("forwardPE")),
        "Debt to Equity": fmt(info.get("debtToEquity")),
        "Volume": fmt(info.get("volume")),
    }

    return render_template("dashboard.html",
                           ticker=ticker,
                           plot_url=plot_url,
                           metrics=metrics)

if __name__ == "__main__":
    app.run(debug=True)
