from flask import jsonify
from .ControllerBase import *
from .BlacklistController import *
from .CapabilityController import *
from .ImageController import *
from .MediaController import *
from .RoleController import *
from .SocialController import *
from .UserController import *
from .VariableController import *

def start_controllers(app, api):
    """Sets all routers of this API. Starts the Resources (Controllers) the will respond the http requests."""

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


    # Resources (controllers)
    api.add_resource(BlacklistController, '/blacklist', '/blacklist/<int:id>')
    api.add_resource(CapabilityController, '/capability', '/capability/<int:id>')
    api.add_resource(MediaController, '/media', '/media/<int:id>')
    api.add_resource(ImageController, '/image/<int:id>')
    api.add_resource(RoleController, '/role', '/role/<int:id>')
    api.add_resource(SocialController, '/social', '/social/<int:id>')
    api.add_resource(UserController, '/user', '/user/<int:id>')
    api.add_resource(VariableController, '/variable', '/variable/<int:id>')