from flask import  request
from flask_restful import Resource, reqparse
from Utils import ErrorHandler

class ControllerBase(Resource):
    """The base class that will provide basics configurations and methods to its children.

    Parameters
    ----------
    Resource: A controller that responses the Resource flask_restful API.
    """

    def __init__(self):
        """Starts the basics request params which are common to many controllers"""

        self.repo = None # must be passed by child controller (namaly, an RepositoryBase child)
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
        """Runs the get http request method response."""

        try:
            return self.repo.get(self.request)
        except Exception as e:
            return ErrorHandler().get_error(405, str(e))


    def post(self):
        """Runs the post http request method response."""

        try:
            return self.repo.create(self.request)
        except Exception as e:
            return ErrorHandler().get_error(405, str(e))


    def put(self, id=None):
        """Runs the get http request method response."""

        try:
            return self.repo.update(id, self.request)
        except Exception as e:
            return ErrorHandler().get_error(405, str(e))


    def delete(self, id=None):
        """Runs the delete http request method response."""

        try:
            return self.repo.delete(id)
        except Exception as e:
            return ErrorHandler().get_error(405, str(e))