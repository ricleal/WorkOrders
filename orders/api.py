
from flask import Flask, request
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

    '''

    def get(self, worker_id):
        ''' not necessary but just for testing '''
        worker = Worker.query.get(worker_id)
        if not worker:
            abort(404, message="Worker {} doesn't exist".format(worker_id))
        else:
            result = worker_schema.dump(worker)
            return result

    def post(self):
        ''' create a worker '''
        data = request.get_json()
        valid = worker_schema.validate(data)
        if valid:
            try:
                w = Worker(
                    name=data['name'],
                    email=data['email']
                )
                db.session.add(w)
                db.session.commit()
            except Exception as e:
                return 'Something wrong', 500    
            return '', 201
        else:
            return 'Unprocessable Entity', 422

    def delete(self, worker_id):
        try:
            worker = Worker.query.get(worker_id)
            print("->", worker)
            db.session.delete(worker)
            db.session.commit()
            return '', 204
        except Exception as e:
            print(str(e))
            return 'Not Found {}'.format(worker_id), 404

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
            result = work_orders_schema.dump(orders)
            return result.data


# https://stackoverflow.com/questions/32419519/get-with-and-without-parameter-in-flask-restful
api.add_resource(WorkerResource, '/worker', '/worker/<int:worker_id>')
api.add_resource(WorkOrderResource, '/workorder', '/workorder/<int:worker_id>')


if __name__ == '__main__':
    app.run(debug=True)
