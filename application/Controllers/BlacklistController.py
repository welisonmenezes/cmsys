from flask import  request
from app import app
from flask_restful import Resource

class BlacklistController(Resource):
    def get(self, id=None):
        return {'message': 'BlacklistController'}, 200