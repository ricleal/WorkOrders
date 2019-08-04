import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

from flask_restful import Api

'''
This module fires up the application.
All methods that should be called before at initialization should go into
`create_app`
'''

db = SQLAlchemy()
logger = logging.getLogger(__name__)


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
    '''
    register the resources: suffix of URLs possible for the REST interface
    '''
    from .resources import WorkerResource, WorkOrderResource
    api.add_resource(WorkerResource, '/worker', '/worker/<int:worker_id>',
                     '/worker/<int:worker_id>/workorder/<int:work_order_id>')
    api.add_resource(WorkOrderResource, '/workorder',
                     '/workorder/worker/<int:worker_id>')


def setup_logging(app):
    ''' Sets the debug logging '''
    if app.debug:
        logger = logging.getLogger()
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(name)s :: %(filename)s:%(lineno)d (%(funcName)s) : '
            '%(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        # the `faker` outputs too much
        logger_faker = logging.getLogger('faker.factory')
        logger_faker.setLevel(logging.INFO)
