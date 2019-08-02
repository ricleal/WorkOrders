from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

from flask_restful import Api

db = SQLAlchemy()
import logging

def create_app(config_class=Config):
    """Construct the core application."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    # app.config.from_pyfile('config.py')

    # Create api
    api = Api(app)

    register_resources(api)
    setup_logging(app)

    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app


def register_resources(api):
    from .resources import WorkerResource, WorkOrderResource
    # https://stackoverflow.com/questions/32419519/get-with-and-without-parameter-in-flask-restful
    api.add_resource(WorkerResource, '/worker', '/worker/<int:worker_id>')
    api.add_resource(WorkOrderResource, '/workorder',
                     '/workorder/<int:worker_id>')


def setup_logging(app):
    logger = logging.getLogger()
    if app.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
