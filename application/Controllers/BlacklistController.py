from flask import  request
from flask_restful import reqparse
from flask_restful import Resource

from Repositories import BlacklistRepository

class BlacklistController(Resource):
    
    def get(self, id=None):
        repo = BlacklistRepository()
        parser = reqparse.RequestParser()
        parser.add_argument('page')
        parser.add_argument('limit')
        parser.add_argument('order')
        parser.add_argument('order_by')
        parser.add_argument('value')
        parser.add_argument('type')
        parser.add_argument('target')
        args = parser.parse_args()
        if id:
            return repo.get_by_id(id)
        else:
            return repo.get(args)

    
    def post(self):
        repo = BlacklistRepository()
        return repo.create(request)


    def put(self, id=None):
        repo = BlacklistRepository()
        return repo.update(id, request)


    def delete(self, id=None):
        repo = BlacklistRepository()
        return repo.delete(id)