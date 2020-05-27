from flask import  request
from ErrorHandlers import ErrorHandler, NotAuthorizedError
from .AuthUtils import *

class BlacklistProtect():

    def __init__(self):

        if str(request.endpoint) == 'ApiBP.blacklistcontroller':

            passport = AuthUtils().get_authorized_passport()
            capabilities = passport['user'].role.capabilities

            if request.method == 'GET':
                AuthUtils().verify_capabilities(capabilities, 'configuration', 'can_read')

            elif request.method == 'POST' or request.method == 'PUT':
                AuthUtils().verify_capabilities(capabilities, 'configuration', 'can_write')

            elif request.method == 'DELETE':
                AuthUtils().verify_capabilities(capabilities, 'configuration', 'can_delete')