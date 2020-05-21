from flask import  request, jsonify
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
            return self.repo.get_by_id(id, self.args) if id else self.repo.get(self.args)
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
            return self.repo.delete(id, self.request)
        except Exception as e:
            return ErrorHandler().get_error(405, str(e))


    @staticmethod
    def error_routers(app):
        """Implements the error routes of the api."""

        # Error 404 handler
        @app.route('/api/<path:path>', defaults={'path': ''})
        def error_404(path):
            return jsonify({
                'error': 404, 
                'message': 'The requested resource does not exist.'
            }), 404


        # Erro 405 handler
        @app.errorhandler(405)
        def error_405(error):
            return jsonify({
                'error': 405,
                'message': 'Method not allowed.'
            }), 405


        # Api root handler
        @app.route('/api/', defaults={'path': ''})
        def index(path):
            return jsonify({
                'message': 'Wellcome to cmsys api v.1.0.0.'
            }), 200


        # Erro 500 handler
        @app.errorhandler(500)
        def error_500(error):
            return jsonify({
                'error': 500,
                'message': 'An internal error has occurred.'
            }), 500