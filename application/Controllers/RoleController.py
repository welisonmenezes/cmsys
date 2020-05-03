from flask import  request
from flask_restful import reqparse
from flask_restful import Resource

from Repositories import RoleRepository

class RoleController(Resource):
    
    def get(self, id=None):
        repo = RoleRepository()
        parser = reqparse.RequestParser()
        parser.add_argument('page')
        parser.add_argument('limit')
        args = parser.parse_args()
        if id:
            return repo.get_by_id(id)
        else:
            return repo.get(args)

    
    def post(self):
        repo = RoleRepository()
        return repo.create(request)


    def put(self, id=None):
        repo = RoleRepository()
        return repo.update(id, request)


    def delete(self, id=None):
        repo = RoleRepository()
        return repo.delete(id)