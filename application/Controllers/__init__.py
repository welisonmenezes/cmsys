from flask import jsonify
from .BlacklistController import BlacklistController
from .VariableController import VariableController

def start_controllers(app, api):

    # Error 404 handler
    @app.route('/api/<path:path>', defaults={'path': ''})
    def error404(path):
        return jsonify({
            'error': 404, 
            'message': 'The requested resource does not exist'
        }), 404

    # Erro 405 handler
    @app.errorhandler(405)
    def error405(error):
        return jsonify({
            'error': 405,
            'message': 'Method not allowed.'
        }), 405

    # Api root handler
    @app.route('/api/', defaults={'path': ''})
    def index(path):
        return jsonify({'message': 'Wellcome to cmsys api v.1.0.0'}), 200

    # Erro 500 handler
    @app.errorhandler(500)
    def error500(error):
        return jsonify({
            'error': 500,
            'message': 'An internal error has occurred'
        }), 500

    # resources
    api.add_resource(BlacklistController, '/blacklist')
    api.add_resource(VariableController, '/variable', '/variable/<int:id>')