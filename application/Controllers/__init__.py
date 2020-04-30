from .BlacklistController import BlacklistController
from .VariableController import VariableController

def start_controllers(api):
    api.add_resource(BlacklistController, '/blacklist')
    api.add_resource(VariableController, '/variable')