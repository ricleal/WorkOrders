from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()


def create_app(config_class=Config):
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_class)
    #app.config.from_pyfile('config.py')

    with app.app_context():
        db.init_app(app)    
        db.create_all()
    
    return app
