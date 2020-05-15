from .ControllerBase import *
from .BlacklistController import *
from .CapabilityController import *
from .ConfigurationController import *
from .LanguageController import *
from .MediaController import *
from .PostTypeController import *
from .RoleController import *
from .SocialController import *
from .TemplateController import *
from .UserController import *
from .VariableController import *


def start_controllers(app, api):
    """Sets all routers of this API. Starts the Resources (Controllers) the will respond the http requests."""

    ControllerBase.error_routers(app)
    
    api.add_resource(BlacklistController, '/blacklist', '/blacklist/<int:id>')
    api.add_resource(CapabilityController, '/capability', '/capability/<int:id>')
    api.add_resource(ConfigurationController, '/configuration', '/configuration/<int:id>')
    api.add_resource(LanguageController, '/language', '/language/<int:id>')
    api.add_resource(MediaController, '/media', '/media/<int:id>', '/media/preview/<int:id>')
    api.add_resource(PostTypeController, '/post-type', '/post-type/<int:id>')
    api.add_resource(RoleController, '/role', '/role/<int:id>')
    api.add_resource(SocialController, '/social', '/social/<int:id>')
    api.add_resource(TemplateController, '/template', '/template/<int:id>')
    api.add_resource(UserController, '/user', '/user/<int:id>')
    api.add_resource(VariableController, '/variable', '/variable/<int:id>')