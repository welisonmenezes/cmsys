from .ControllerBase import *
from .BlacklistController import *
from .CapabilityController import *
from .CommentController import *
from .ConfigurationController import *
from .FieldController import *
from .FieldContentController import *
from .FieldFileController import *
from .FieldTextController import *
from .GrouperController import *
from .LanguageController import *
from .MediaController import *
from .MenuController import *
from .MenuItemController import *
from .NestController import *
from .PostController import *
from .PostTypeController import *
from .RoleController import *
from .SectorController import *
from .SocialController import *
from .TemplateController import *
from .TermController import *
from .UserController import *
from .VariableController import *


def start_controllers(app, api):
    """Sets all routers of this API. Starts the Resources (Controllers) the will respond the http requests."""

    ControllerBase.default_routers(app)
    
    api.add_resource(BlacklistController, '/blacklist', '/blacklist/<int:id>')
    api.add_resource(CapabilityController, '/capability', '/capability/<int:id>')
    api.add_resource(CommentController, '/comment', '/comment/<int:id>')
    api.add_resource(ConfigurationController, '/configuration', '/configuration/<int:id>')
    api.add_resource(FieldController, '/field', '/field/<int:id>')
    api.add_resource(FieldContentController, '/field-content', '/field-content/<int:id>')
    api.add_resource(FieldFileController, '/field-file', '/field-file/<int:id>')
    api.add_resource(FieldTextController, '/field-text', '/field-text/<int:id>')
    api.add_resource(GrouperController, '/grouper', '/grouper/<int:id>')
    api.add_resource(LanguageController, '/language', '/language/<int:id>')
    api.add_resource(MediaController, '/media', '/media/<id>', '/media/preview/<id>', '/media/suggestions/<name>')
    api.add_resource(MenuController, '/menu', '/menu/<int:id>')
    api.add_resource(MenuItemController, '/menu-item', '/menu-item/<int:id>')
    api.add_resource(NestController, '/nest', '/nest/<int:id>')
    api.add_resource(PostController, '/post', '/post/<id>', '/post/suggestions/<name>')
    api.add_resource(PostTypeController, '/post-type', '/post-type/<int:id>')
    api.add_resource(RoleController, '/role', '/role/<int:id>')
    api.add_resource(SectorController, '/sector', '/sector/<int:id>')
    api.add_resource(SocialController, '/social', '/social/<int:id>')
    api.add_resource(TemplateController, '/template', '/template/<int:id>')
    api.add_resource(TermController, '/term', '/term/<int:id>', '/term/suggestions/<name>')
    api.add_resource(UserController, '/user', '/user/<int:id>')
    api.add_resource(VariableController, '/variable', '/variable/<int:id>')