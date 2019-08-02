import ast
import os

import dotenv
dotenv.load_dotenv()

class Config:
    pass

class ProductionConfig(Config):
    FLASK_DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    APPLICATION_ROOT = '/api/v1'

class DevelopmentConfig(Config):
    FLASK_DEBUG = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/orders.db'
    TESTING = False
    DEBUG = True # LOG
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APPLICATION_ROOT = None

class TestingConfig(DevelopmentConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    APPLICATION_ROOT = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False