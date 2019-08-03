import os

import dotenv

'''
Configure the several enviroments where this application can run.
Note that heroku doesn't like `.env` files. They have to copied every time
the app is deployed.
For test purposes use:
`os.getenv(<env variable>, <default>)`
with a default value
'''

dotenv.load_dotenv()


class Config:
    pass


class ProductionConfig(Config):
    FLASK_DEBUG = False
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        r";v:<6KVX^(zprT>/SC8#)w(Pn8W`RbBTH-pqGA;u(,tGF95vXduyUy(p7rB@H:")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///orders.db")
    APPLICATION_ROOT = '/api/v1'


class DevelopmentConfig(Config):
    FLASK_DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY", "Rx7mrFRZkzUVyXtZusWCYSs88RsQpVam")
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/orders.db'
    TESTING = False
    DEBUG = True  # LOG
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APPLICATION_ROOT = None


class TestingConfig(DevelopmentConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    APPLICATION_ROOT = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
