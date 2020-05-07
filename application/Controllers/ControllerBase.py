from flask import  request
from flask_restful import Resource
from flask_restful import reqparse

class ControllerBase(Resource):

    def __init__(self):
        self.request = request
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('page')
        self.parser.add_argument('limit')
        self.parser.add_argument('order')
        self.parser.add_argument('order_by')
        self.parser.add_argument('date_modifier')

    
    # TODO: get, post, put and delete methods to be overloaded by your children