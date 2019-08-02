  
from jsonschema import validate
import os
import json
from flask import request, jsonify, abort
from jsonschema.exceptions import ValidationError



worker_dic_schema = {
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

work_order_dic_schema = {
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
            "pattern": r"^\d{4}-\d{1,2}-\d{1,2}$"
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


def validator_decorator(schema_dic):
    def decorator(func):
        ''' Validator decorator to use in Flask '''
        def func_wrapper(*args, **kwargs):
            json_data = request.get_json(force=True)
            try:
                validate(instance=json_data, schema=schema_dic)
            except ValidationError:
                return abort(422)
            return func(*args, **kwargs)
        return func_wrapper
    return decorator