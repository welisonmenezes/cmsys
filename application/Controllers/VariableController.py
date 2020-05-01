from flask import  request
from flask_restful import Resource

from Repositories import VariableRepository

class VariableController(Resource):

    def get(self, id=None):

        repo = VariableRepository()

        if id:
            return repo.getByID(id)
        else:
            return repo.getAll()