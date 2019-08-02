import ast
import os

import dotenv
dotenv.load_dotenv()


class Config:
    FLASK_DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
    APPLICATION_ROOT = '/api/v1'


class TestingConfig(Config):
    FLASK_DEBUG = True
    SQLALCHEMY_DATABASE_URI =  os.getenv("DATABASE_URI")
    #'sqlite:///:memory:'
    TESTING = True
    DEBUG = True # LOG
    APPLICATION_ROOT = ''