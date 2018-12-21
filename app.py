from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# local dev config:
# from config import Config
# app.config.from_object(Config)

# heroku config:
from flask_heroku import Heroku
heroku = Heroku(app)

db = SQLAlchemy(app)
data = []


@app.route("/")
def home():
    return render_template("index.html", stockdata=data)


@app.route("/", methods=["POST"])
def main():
    from models import StockData
    global data
    filters = "mean_price_target_diff IS NOT NULL"
    if request.form:
        price_min = request.form.get("price-min")
        price_max = request.form.get("price-max")
        n_min = request.form.get("n-min")

        if price_min != '':
            filters += " AND price >= {}".format(price_min)

        if price_max != '':
            filters += " AND price <= {}".format(price_max)

        if n_min != '':
            filters += " AND n >= {}".format(n_min)

    data = StockData.query.filter(filters)
    return render_template("index.html", stockdata=data)


if __name__ == "__main__":
    app.run()
