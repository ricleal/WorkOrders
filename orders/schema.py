from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

from .model import Worker, WorkOrder
from . import db


class WorkerSchema(ModelSchema):
    class Meta:
        model = Worker


class WorkOrderSchema(ModelSchema):

    workers = fields.Nested(
        # Exclude in the target model
        WorkerSchema, many=True, exclude=("workers")
    )

    class Meta:
        model = WorkOrder
        sqla_session = db.session


worker_schema = WorkerSchema(transient=True)
work_order_schema = WorkOrderSchema()
work_orders_schema = WorkOrderSchema(many=True)


worker_schema2 = {
    "definitions": {},
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://example.com/root.json",
    "type": "object",
    "title": "The Root Schema",
    "required": [
        "name",
        "email"
    ],
    "properties": {
        "name": {
            "$id": "#/properties/name",
            "type": "string",
            "title": "The Name Schema",
            "default": "",
            "examples": [
                "Lisa Freeman"
            ],
            "pattern": "^(.*)$"
        },
        "email": {
            "$id": "#/properties/email",
            "type": "string",
            "title": "The Email Schema",
            "default": "",
            "examples": [
                "stephenbuckley@bond.com"
            ],
            "pattern": "^(.*)$"
        }
    }
}

work_order_schema2 = {
    "definitions": {},
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://example.com/root.json",
    "type": "object",
    "title": "The Root Schema",
    "required": [
        "deadline",
        "title",
    ],
    "properties": {
        "deadline": {
            "$id": "#/properties/deadline",
            "type": "string",
            "title": "The Deadline Schema",
            "default": "",
            "examples": [
                "2013-06-04"
            ],
            "pattern": r"^d{4}-\d{1,2}-\d{1,2}$"
        },
        "title": {
            "$id": "#/properties/title",
            "type": "string",
            "title": "The Title Schema",
            "default": "",
            "examples": [
                "Them paper level her last."
            ],
            "pattern": "^(.*)$"
        },
        "description": {
            "$id": "#/properties/description",
            "type": "string",
            "title": "The Description Schema",
            "default": "",
            "examples": [
                "Seek throw reality dark argue cold near all. Any feel well certainly time support bed night.\nSort here mother be ok. Once research town short media two.\nSmall home big account woman most various president. Interest project forget forget hundred game special world.\nPolicy thought probably player usually girl. Activity in line military past nature heart. Democratic pretty response single.\nFigure down chance young. Help base ok indeed article security worry son.\nMay may market option. Law wrong training save.\nReally election left son girl man. Writer bar before near region marriage.\nInternational everybody allow war. Reason most value just."
            ],
            "pattern": "^(.*)$"
        }
    }
}
