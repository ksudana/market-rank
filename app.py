from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import models
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

data = []


@app.route("/")
def home():
    return render_template("index.html", stockdata=data)


@app.route("/", methods=["POST"])
def main():
    global data
    filters = "mean_price_target_diff IS NOT NULL"
    if request.form:
        price_filter = request.form.get("price-filter")
        price_value = request.form.get("price-value")
        if price_value != '':
            filters += " AND price " + price_filter + " " + price_value

    data = models.StockData.query.filter(filters)
    return render_template("index.html", stockdata=data)


if __name__ == "__main__":
    app.run()
