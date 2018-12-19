from app import db


# Realtime data
class StockData(db.Model):
    symbol = db.Column(db.String(6), unique=True, nullable=False, primary_key=True)
    price = db.Column(db.Float)
    mean_price_target_diff = db.Column(db.Float, nullable=True)
    mean_analyst_rating = db.Column(db.Integer, nullable=True)
    n = db.Column(db.Integer)

    def __repr__(self):
        return "<Symbol: {}, Price {}>".format(self.symbol, self.price)


# Metadata
class StockMD(db.Model):
    symbol = db.Column(db.String(6), unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(100))
    sector = db.Column(db.String(30))

    def __repr__(self):
        return "<Symbol: {}, Name: {}>".format(self.symbol, self.name)
