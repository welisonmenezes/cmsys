from flask import  request
from ErrorHandlers import ErrorHandler, NotAuthorizedError
from .AuthUtils import *

class BlacklistProtect():

    def __init__(self):

        print(request.method)
        print(request.url_rule)

        if str(request.url_rule) == '/api/blacklist/<int:id>':
            passport = AuthUtils().get_authorized_passport()
            print(passport)
            #raise NotAuthorizedError('You do not have permission to access this resource.')