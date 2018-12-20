import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/marketdata'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
