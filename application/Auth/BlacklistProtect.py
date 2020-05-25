from flask import  request
from ErrorHandlers import ErrorHandler, NotAuthorizedError

class BlacklistProtect():

    def __init__(self):
        pass
        #print(request.method)
        #print(request.url_rule)

        #if str(request.url_rule) == '/api/xblacklist/<int:id>':
            #raise NotAuthorizedError('You do not have permission to access this resource.')