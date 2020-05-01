from flask import jsonify
from .BlacklistController import BlacklistController
from .VariableController import VariableController

def start_controllers(app, api):

    # Error 404 handler
    @app.route('/api/<path:path>', defaults={'path': ''})
    def error404(path):
        return jsonify({'message': 'The requested resource does not exist'}), 404

    # Api root handler
    @app.route('/api/', defaults={'path': ''})
    def index(path):
        return jsonify({'message': 'Wellcome to cmsys api v.1.0.0'}), 200

    # Erro 500 handler
    @app.errorhandler(500)
    def error500(error):
        return jsonify({'message': 'An internal error has occurred'}), 500

    # resources
    api.add_resource(BlacklistController, '/blacklist')
    api.add_resource(VariableController, '/variable')