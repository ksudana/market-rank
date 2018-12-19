import os
from models import db

os.remove("marketdata.db")
db.create_all()
