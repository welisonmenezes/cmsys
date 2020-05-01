from flask import  request
from flask_restful import Resource

from Repositories import VariableRepository

class VariableController(Resource):

    def get(self, id=None):

        repo = VariableRepository()

        if id:
            return repo.get_by_id(id)
        else:
            return repo.get()

    
    def post(self):
        
        repo = VariableRepository()

        return repo.create(request)