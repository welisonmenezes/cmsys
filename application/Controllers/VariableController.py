from flask import  request
from app import app
from flask_restful import Resource

from Models.DBSession import Session
from Models.DBContext import Variable
from Models.DBSchema import VariableSchema

class VariableController(Resource):
    def get(self, id=None):

        session = Session()
        schema = VariableSchema(many=True)
        result = session.query(Variable).all()
        data = schema.dump(result)
        session.close()

        return {
            'data': data
        }, 200