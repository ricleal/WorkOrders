import logging
from datetime import datetime

from flask import request
from flask_restful import Resource, abort
from sqlalchemy import asc
from sqlalchemy.exc import SQLAlchemyError

from . import db
from .model import Worker, WorkOrder
from .schema import work_orders_schema, worker_schema
from .validator import (validator_decorator, work_order_dic_schema,
                        worker_dic_schema)

'''
This is the heart of the RESTFul application.
'''

logger = logging.getLogger(__name__)
MAX_NUMBER_OF_WORKERS_PER_WORK_ORDER = 5


class WorkerResource(Resource):
    '''
    All the worker related REST actions are coded here
    '''

    def get(self, worker_id):
        ''' not necessary but just for testing '''
        try:
            worker = Worker.query.get(worker_id)
        except SQLAlchemyError as e:
            logger.error(e)
            return 'Something wrong: {}'.format(str(e)), 500
        if not worker:
            message = "Worker {} does not exist".format(worker_id)
            logger.warning(message)
            abort(404, message=message)
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
                company=data['company'],
                email=data['email']
            )
            db.session.add(w)
            db.session.commit()
            logger.info("Worker created: {}".format(w))
            return w.id, 201
        except SQLAlchemyError as e:
            logger.error(e)
            return 'Something wrong: {}'.format(str(e)), 500

    def delete(self, worker_id):
        ''' delete a worker '''
        try:
            worker = Worker.query.get(worker_id)
            if not worker:
                message = "Worker {} does not exist".format(worker_id)
                logger.warning(message)
                abort(404, message=message)
            else:
                db.session.delete(worker)
                db.session.commit()
                logger.info('Worker deleted: {}'.format(worker))
                return '', 204
        except SQLAlchemyError as e:
            logger.error(e)
            return 'Something wrong: {}'.format(worker_id), 404

    def put(self, worker_id, work_order_id):
        ''' Assigning a worker to an order
        A max of 5 workers can work on one order
        updates worker: w1.worker_orders.append(wo1)'''
        try:
            n_workers = db.session.query(WorkOrder).join(
                WorkOrder.workers).filter(WorkOrder.id ==
                                          work_order_id).count()
            if n_workers >= MAX_NUMBER_OF_WORKERS_PER_WORK_ORDER:
                message = ("The work order {} is full. You only can have {} "
                           "workers per work order".format(
                               work_order_id,
                               MAX_NUMBER_OF_WORKERS_PER_WORK_ORDER))
                logger.warning(message)
                return abort(404, message=message)
            else:
                work_order = WorkOrder.query.get(work_order_id)
                worker = Worker.query.get(worker_id)
                worker.worker_orders.append(work_order)
                db.session.commit()
                logger.info("Worker {} assigned to order {}.".format(
                    worker, work_order))
                return '', 200
        except SQLAlchemyError as e:
            logger.error(e)
            return 'Something wrong happened: {}'.format(e), 404


class WorkOrderResource(Resource):
    '''
    All the Work Order related REST actions are coded here
    '''

    def get(self, worker_id=None):
        ''' Fetch all work orders:
            - For a specific worker
            - Sorted by deadline '''
        logger.debug("WorkOrderResource GET: {}".format(worker_id))
        if worker_id is None:
            logger.debug("Getting all work orders...")
            try:
                orders = WorkOrder.query.order_by(asc(
                    WorkOrder.deadline)).all()
            except SQLAlchemyError as e:
                logger.error(e)
                return 'Something wrong happened: {}'.format(e), 404
            result = work_orders_schema.dump(orders)
            return result.data
        else:
            logger.debug("Getting work orders for worker.id = {}".format(
                worker_id))
            try:
                orders = WorkOrder.query.filter(
                    WorkOrder.workers.any(id=worker_id)).all()
            except SQLAlchemyError as e:
                orders = []
                logger.error(e)
                return 'Something wrong happened: {}'.format(e), 404
            if not orders:
                message = "No Work Order exists for worker {}".format(
                    worker_id)
                logger.warning(message)
                abort(404, message=message)
            result = work_orders_schema.dump(orders)
            return result.data

    @validator_decorator(work_order_dic_schema)
    def post(self):
        ''' create a work order '''
        data = request.get_json()
        try:
            wo = WorkOrder(
                title=data['title'],
                description=data.get('description', ''),  # optional
                deadline=datetime.strptime(
                    data['deadline'], "%Y-%m-%d").date(),
            )
            db.session.add(wo)
            db.session.commit()
            logger.info("Work Orderer created: {}".format(wo))
            return wo.id, 201
        except SQLAlchemyError as e:
            logger.error(e)
            return 'Something wrong: {}'.format(str(e)), 500
