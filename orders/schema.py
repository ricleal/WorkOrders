from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

from .model import Worker, WorkOrder
from . import db


class WorkerSchema(ModelSchema):

    class Meta:
        model = Worker
        sqla_session = db.session


class WorkOrderSchema(ModelSchema):

    workers = fields.Nested(
        # Exclude in the target model
        WorkerSchema, many=True, exclude=("workers")
    )

    class Meta:
        model = WorkOrder
        sqla_session = db.session


worker_schema = WorkerSchema()
work_order_schema = WorkOrderSchema()
work_orders_schema = WorkOrderSchema(many=True)
