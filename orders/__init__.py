import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

from flask_restful import Api

db = SQLAlchemy()


def create_app(config_class=Config):
    """Construct the core application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Create restful api (this the only way to have the prefix)
    api = Api(app, prefix=app.config['APPLICATION_ROOT'])

    register_resources(api)
    setup_logging(app)

    with app.app_context():
        db.init_app(app)
        db.create_all()

    return app


def register_resources(api):
    from .resources import WorkerResource, WorkOrderResource
    # https://stackoverflow.com/questions/32419519/get-with-and-without-parameter-in-flask-restful
    api.add_resource(WorkerResource, '/worker', '/worker/<int:worker_id>',
                     '/worker/<int:worker_id>/<int:work_order_id>')
    api.add_resource(WorkOrderResource, '/workorder',
                     '/workorder/<int:worker_id>')


def setup_logging(app):
    if app.debug:
        logging.basicConfig(level=logging.DEBUG)
        app.logger.setLevel(logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
