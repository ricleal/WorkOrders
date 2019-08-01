import ast
import os

import dotenv
dotenv.load_dotenv()


class Config:
    FLASK_DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")

class TestingConfig(Config):
    FLASK_DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
