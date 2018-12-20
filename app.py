from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku

#from config import Config

app = Flask(__name__)
#app.config.from_object(Config)
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
        price_filter = request.form.get("price-filter")
        price_value = request.form.get("price-value")
        if price_value != '':
            filters += " AND price " + price_filter + " " + price_value

    data = StockData.query.filter(filters)
    return render_template("index.html", stockdata=data)


if __name__ == "__main__":
    app.run()
