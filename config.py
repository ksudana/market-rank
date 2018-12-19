import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(os.path.join(basedir, "marketdata.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False