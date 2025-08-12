from flask import Flask, render_template, request
import yfinance as yf
import pandas as pd

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

if __name__ == "__main__":
    app.run(debug=True)
