
from flask import Flask
from flask_restful import Api, Resource, abort, reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

from . import db, create_app
from .model import Worker, WorkOrder
from .schema import work_order_schema, work_orders_schema, worker_schema


app = create_app()
api = Api(app)


class WorkerResource(Resource):
    '''
    Class that handles REST for '/books/<int:book_id>'
    get, delete and put (update)
    '''

    def post(self):
        ''' create a worker '''
        pass

    def delete(self, worker_id):
        pass

    def put(self, worker_id):
        ''' Assigning a worker to an order
        updates worker: w1.worker_orders.append(wo1)'''
        pass


class WorkOrderResource(Resource):

    def get(self, worker_id=None):
        ''' Fetch all work orders:
            - For a specific worker
            - Sorted by deadline '''
        if worker_id is None:
            # Sorted by deadline
            orders = WorkOrder.query.order_by(desc(
                WorkOrder.deadline)).all()
            result = work_orders_schema.dump(orders)
            return result.data

        else:
            orders = WorkOrder.query.filter(
                WorkOrder.workers.any(id=worker_id)).all()
            result=work_orders_schema.dump(orders)
            return result.data


# https://stackoverflow.com/questions/32419519/get-with-and-without-parameter-in-flask-restful
api.add_resource(WorkerResource, '/worker', '/worker/<int:worker_id>')
api.add_resource(WorkOrderResource, '/workorder', '/workorder/<int:worker_id>')


if __name__ == '__main__':
    app.run(debug = True)
