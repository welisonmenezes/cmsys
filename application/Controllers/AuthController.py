from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from app import bcrypt
from ErrorHandlers import ErrorHandler
from Models import Session, User

class AuthController(Resource):
    """This flask_restful API's Resource works like a controller to AuthRepository."""

    def __init__(self):
        self.session = Session()
    

    def get(self, id=None):
        
        if str(request.url_rule) == '/api/public':

            try:
                access = decode_token('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTA1MDYwMzQsIm5iZiI6MTU5MDUwNjAzNCwianRpIjoiZTFmN2MxZjgtNzBmYy00YmU4LTg2NWQtYjFkNDAyN2NkOWRkIiwiZXhwIjoxNTkwNTA2MjE0LCJpZGVudGl0eSI6eyJpZCI6MSwibG9naW4iOiJhZG1pbiIsInJvbGUiOiJBZG1pbmlzdHJhdG9yIn0sImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.B5-k4DL3fkY3ZkupgdQ6feXzP36q5UM5dvKQESr9xSA')

                if 'identity' in access:

                    return access

            except Exception as e:
                
                return 'refaça seu login'


    def post(self):

        if str(request.url_rule) == '/api/login':
            return self._login()
        elif str(request.url_rule) == '/api/refresh':
            return self._refresh()
        
        return ErrorHandler().get_error(405, 'Method not allowed.')



    def _login(self):
        """"""

        data = request.get_json()
        if 'login' in data and 'password' in data and data['login'] != '' and data['password'] != '':
            user = self.session.query(User).filter_by(login=data['login']).first()
            if user:
                if bcrypt.check_password_hash(user.password, data['password']):
                    user_identity = {
                        'id': user.id,
                        'login': user.login,
                        'role': user.role.name
                    }
                    try:
                        token = create_access_token(identity=user_identity)
                        refresh_token = create_refresh_token(identity=user_identity)
                        user.refresh_token = refresh_token
                        self.session.commit()
                        return {
                            'access_token': token,
                            'refresh_token': refresh_token
                        }, 200
                    except Exception as e:
                        return ErrorHandler().get_error(500, 'Error to process your login.')
                else:
                    return ErrorHandler().get_error(401, 'Invalid credencials.')
            else:
                return ErrorHandler().get_error(401, 'Invalid credencials.')
        else:
            return ErrorHandler().get_error(400, 'Insufficient data to authenticate.')


    def _refresh(self):
        """"""

        data = request.get_json()
        if 'refresh_token' in data and data['refresh_token'] != '':
            try:
                access = decode_token(data['refresh_token'])
                if 'identity' in access:
                    identity = access['identity']
                    if 'id' in identity and 'login' in identity and 'role' in identity:
                        user = self.session.query(User).filter_by(login=identity['login']).first()
                        if user:
                            if user.refresh_token == data['refresh_token']:
                                try:
                                    token = create_access_token(identity=identity)
                                    refresh_token = create_refresh_token(identity=identity)
                                    user.refresh_token = refresh_token
                                    self.session.commit()
                                    return {
                                        'access_token': token,
                                        'refresh_token': refresh_token
                                    }, 200
                                except Exception as e:
                                    return ErrorHandler().get_error(500, 'Error to process the token refreshing.')
                            else:
                                return ErrorHandler().get_error(401, 'The given Refresh Token is not available.')
                        else:
                            return ErrorHandler().get_error(400, 'No user found.')
                    else:
                        return ErrorHandler().get_error(400, 'Invalid identity.')
                else:
                    return ErrorHandler().get_error(400, 'Invalid Refresh Token.')
            except Exception as e:
                return ErrorHandler().get_error(401, 'Refresh Token expired.')
        else:
            return ErrorHandler().get_error(400, 'No Refresh Token send.')