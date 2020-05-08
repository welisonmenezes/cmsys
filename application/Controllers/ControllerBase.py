from flask import  request
from flask_restful import Resource, reqparse
from Utils import ErrorHandler

class ControllerBase(Resource):

    def __init__(self):
        self.request = request
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('page')
        self.parser.add_argument('limit')
        self.parser.add_argument('order')
        self.parser.add_argument('order_by')
        self.parser.add_argument('date_modifier')
        self.parser.add_argument('compare_date_time_one')
        self.parser.add_argument('compare_date_time_two')
        self.parser.add_argument('not_between')

    
    def get(self, id=None):
        return ErrorHandler(405, 'This method must be implemented by a child class.').response


    def post(self):
        return self.repo.create(self.request)


    def put(self, id=None):
        return self.repo.update(id, self.request)


    def delete(self, id=None):
        return self.repo.delete(id)