from flask import  request, jsonify
from flask_restful import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException
from ErrorHandlers import ErrorHandler, NotAuthorizedError, BadRequestError, NotFoundError
from Utils import Helper
from Auth import protect_endpoints
from Models import Session

class ControllerBase(Resource):
    """The base class that will provide basics configurations and methods to its children.

    Parameters
    ----------
    Resource: A controller that responses the Resource flask_restful API.
    """

    def __init__(self):
        """Starts the basics request params which are common to many controllers"""

        self.repo = None # must be passed by child controller (nemaly, an RepositoryBase child)
        self.request = request
        self.parser = reqparse.RequestParser()
        self.session = Session()
        Helper().add_request_data(self.parser, [
            'page', 'limit', 'order', 'order_by', 'date_modifier', 
            'compare_date_time_one', 'compare_date_time_two', 'not_between'],
        False)

    
    def get(self, id=None):
        """Runs the get http request method response."""

        def fn():
            return self.repo.get_by_id(id, self.args) if id else self.repo.get(self.args)
        return ControllerBase.run_if_not_raise(fn, self.session)


    def post(self):
        """Runs the post http request method response."""

        def fn():
            return self.repo.create(self.request)
        return ControllerBase.run_if_not_raise(fn, self.session)


    def put(self, id=None):
        """Runs the get http request method response."""

        def fn():
            return self.repo.update(id, self.request)
        return ControllerBase.run_if_not_raise(fn, self.session)


    def delete(self, id=None):
        """Runs the delete http request method response."""

        def fn():
            return self.repo.delete(id, self.request)
        return ControllerBase.run_if_not_raise(fn, self.session)


    @staticmethod
    def default_routers(app):
        """Implements the error routes of the api."""

        @app.before_request
        def before_request():
            """Before request execute the endpoint protectors."""
            
            def fn():
                protect_endpoints()
            return ControllerBase.run_if_not_raise(fn)
                

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


    @staticmethod
    def run_if_not_raise(fn, session=None):
        """Catch exception if it occurs, if not, execute the given function."""

        try:
            return fn()
        except NotAuthorizedError as e:
            return ErrorHandler().get_error(401, e.message)
        except BadRequestError as e:
            return ErrorHandler().get_error(400, e.message)
        except NotFoundError as e:
            return ErrorHandler().get_error(404, e.message)
        except Exception as e:
            return ErrorHandler().get_error(500, str(e))
        except SQLAlchemyError as e:
            return ErrorHandler().get_error(500, str(e))
        except HTTPException as e:
            return ErrorHandler().get_error(500, str(e))
        except AttributeError as e:
            return ErrorHandler().get_error(500, str(e))
        except Exception as e:
            return ErrorHandler().get_error(500, str(e))
        finally:
            if session:
                session.rollback()