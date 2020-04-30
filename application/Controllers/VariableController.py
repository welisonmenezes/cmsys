from flask import  request
from app import app
from flask_restful import Resource

class VariableController(Resource):
    def get(self, id=None):
        return {'message': 'VariableController'}, 200