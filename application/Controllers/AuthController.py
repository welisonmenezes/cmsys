from flask import jsonify, request
from flask_restful import Resource

from flask_jwt_extended import (jwt_required, create_access_token, jwt_refresh_token_required, 
create_refresh_token, get_jwt_identity, current_user, decode_token)

class AuthController(Resource):
    """This flask_restful API's Resource works like a controller to AuthRepository."""
    

    def get(self, id=None):
        
        if str(request.url_rule) == '/api/public':

            try:
                access = decode_token('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTA0NTI1MjAsIm5iZiI6MTU5MDQ1MjUyMCwianRpIjoiNzg0OWQ5NjAtZjQ5Mi00Mjc5LTgyNzAtOTY0M2EyMTY3YzdkIiwiZXhwIjoxNTkwNDUyNTUwLCJpZGVudGl0eSI6IndlbGlzb24iLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.RAHDNc45miHdNz9-Zm2ZR30mYVp5fBz6pp4ayBmWSHA')

                if 'identity' in access:

                    return 'pode acessar'

            except Exception as e:
                
                return 'refaça seu login'


    def post(self):
        
        if str(request.url_rule) == '/api/login':
            return self._login()
        elif str(request.url_rule) == '/api/refresh':
            return self._refresh()

        
        return ret, 200



    def _login(self):
        username = 'welison'
        password = '123456'

        if username != 'welison' or password != '123456':
            return {'message': 'erooooou'}, 401

        return {
            'access_token': create_access_token(identity=username),
            'refresh_token': create_refresh_token(identity=username)
        }, 200


    def _refresh(self):

        try:
            access = decode_token('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTA0NTI1MjAsIm5iZiI6MTU5MDQ1MjUyMCwianRpIjoiZmE4MzQ4MDUtODg5Ni00OGJhLWI3Y2MtZTZlNjg2MTQ5MTJjIiwiZXhwIjoxNTkwNDUyNTgwLCJpZGVudGl0eSI6IndlbGlzb24iLCJ0eXBlIjoicmVmcmVzaCJ9.vw9G0m6AMpTzeDqD_t8PbH9S-wEki9k4ZfRrRvoLyj0')

            if 'identity' in access:
                return {
                    'access_token': create_access_token(identity=access['identity'])
                }, 200

        except Exception as e:
            
            return 'sem acesso'

        
