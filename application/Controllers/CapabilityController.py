from flask import  request
from flask_restful import reqparse
from flask_restful import Resource

from Repositories import CapabilityRepository

class CapabilityController(Resource):
    
    def get(self, id=None):
        repo = CapabilityRepository()
        parser = reqparse.RequestParser()
        parser.add_argument('page')
        parser.add_argument('limit')
        parser.add_argument('description')
        parser.add_argument('type')
        parser.add_argument('target_id')
        parser.add_argument('can_write')
        parser.add_argument('can_read')
        parser.add_argument('can_delete')
        args = parser.parse_args()
        if id:
            return repo.get_by_id(id)
        else:
            return repo.get(args)

    
    def post(self):
        repo = CapabilityRepository()
        return repo.create(request)


    def put(self, id=None):
        repo = CapabilityRepository()
        return repo.update(id, request)


    def delete(self, id=None):
        repo = CapabilityRepository()
        return repo.delete(id)