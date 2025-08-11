from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Привет! Это начало моего дипломного проекта."

if __name__ == "__main__":
    app.run(debug=True)
