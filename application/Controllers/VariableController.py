from flask import  request
from flask_restful import reqparse
from flask_restful import Resource

from Repositories import VariableRepository

class VariableController(Resource):

    def get(self, id=None):
        repo = VariableRepository()
        parser = reqparse.RequestParser()
        parser.add_argument('s')
        args = parser.parse_args()
        if id:
            return repo.get_by_id(id)
        else:
            return repo.get(args)

    
    def post(self):
        repo = VariableRepository()
        return repo.create(request)


    def put(self, id=None):
        repo = VariableRepository()
        return repo.update(id, request)


    def delete(self, id=None):
        repo = VariableRepository()
        return repo.delete(id)