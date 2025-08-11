from flask import Flask, render_template

app = Flask(__name__)

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Страница со списком акций
@app.route('/stocks')
def stocks():
    return "Здесь будут данные по акциям"

if __name__ == '__main__':
    app.run(debug=True)
