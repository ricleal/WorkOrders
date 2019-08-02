import logging

from flask import request
from flask_restful import Resource, abort, reqparse
from sqlalchemy import desc
from datetime import datetime
from pprint import pformat
from . import db
from .model import Worker, WorkOrder
from .schema import work_order_schema, work_orders_schema, worker_schema
from .validator import worker_dic_schema, work_order_dic_schema, validator_decorator
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

    @validator_decorator(worker_dic_schema)
    def post(self):
        ''' create a worker '''
        data = request.get_json()
        try:
            w = Worker(
                name=data['name'],
                email=data['email']
            )
            db.session.add(w)
            db.session.commit()
            logger.debug("GET: {}".format(w))
            return w.id, 201
        except Exception as e:
            logger.error(str(e))
            return 'Something wrong: {}'.format(str(e)), 500

    def delete(self, worker_id):
        try:
            worker = Worker.query.get(worker_id)
            logger.debug('Delete: {}'.format(worker))
            db.session.delete(worker)
            db.session.commit()
            return '', 204
        except Exception as e:
            logger.error(str(e))
            return 'Not Found {}'.format(worker_id), 404

    def put(self, worker_id, work_order_id):
        ''' Assigning a worker to an order
        A max of 5 workers can work on one order
        updates worker: w1.worker_orders.append(wo1)'''
        try:
            n_workers = db.session.query(WorkOrder).join(
                WorkOrder.workers).filter(WorkOrder.id == work_order_id).count()
            if n_workers >= 5:
                return {"message": "Order is full"}, 404
            else:
                work_order = WorkOrder.query.get(work_order_id)
                worker = Worker.query.get(worker_id)
                worker.worker_orders.append(work_order)
                db.session.commit()
                return {"message": "Worker {} assigned to order {}.".format(
                    worker, work_order)}, 200
        except Exception as e:
            logger.error(str(e))
            return 'Something wrong happened: {}'.format(e), 404


class WorkOrderResource(Resource):

    def get(self, worker_id=None):
        ''' Fetch all work orders:
            - For a specific worker
            - Sorted by deadline '''
        if worker_id is None:
            logger.debug("Getting all orders...")
            orders = WorkOrder.query.order_by(desc(
                WorkOrder.deadline)).all()
            result = work_orders_schema.dump(orders)
            return result.data

        else:
            logger.debug("Getting order for worker: {}".format(worker_id))
            orders = WorkOrder.query.filter(
                WorkOrder.workers.any(id=worker_id)).all()
            result = work_orders_schema.dump(orders)
            # logger.debug(pformat(result.data))
            return result.data

    @validator_decorator(work_order_dic_schema)
    def post(self):
        ''' create a worker '''
        data = request.get_json()
        try:
            wo = WorkOrder(
                title=data['title'],
                description=data['description'],
                deadline=datetime.strptime(
                    data['deadline'], "%Y-%m-%d").date(),
            )
            db.session.add(wo)
            db.session.commit()
            logger.debug("POST: {}".format(wo))
            return wo.id, 201
        except Exception as e:
            logger.error(str(e))
            return 'Something wrong: {}'.format(str(e)), 500
