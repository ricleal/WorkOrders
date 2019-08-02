from flask import request
from flask_restful import Resource, abort, reqparse
from sqlalchemy import desc

from . import db
from .model import Worker, WorkOrder
from .schema import work_order_schema, work_orders_schema, worker_schema

import logging
logger = logging.getLogger(__name__)

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
        validation_dict = worker_schema.validate(data)
        if validation_dict == {}:
            try:
                w = Worker(
                    name=data['name'],
                    email=data['email']
                )
                db.session.add(w)
                db.session.commit()
                logger.debug(w)
            except Exception as e:
                return 'Something wrong: {}'.format(str(e)), 500
            logger.debug("Validation successful")
            return '', 201
        else:
            return 'Validation Error: {}'.format(validation_dict), 422

    def delete(self, worker_id):
        try:
            worker = Worker.query.get(worker_id)
            logger.debug('this is a DEBUG message')
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
