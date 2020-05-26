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
                access = decode_token('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTA1MDU0MjksIm5iZiI6MTU5MDUwNTQyOSwianRpIjoiYTg3YWM4NmYtMDJmMi00Nzk0LTg1MzktMDRiM2YyN2U1OWM0IiwiZXhwIjoxNTkwNTA1NjA5LCJpZGVudGl0eSI6eyJpZCI6MSwibG9naW4iOiJhZG1pbiIsInJvbGUiOiJBZG1pbmlzdHJhdG9yIn0sImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.rExyjtVG2NQAUw-DvxOSKoVfcsOyGJgihkDc46RvRC4')

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
                        refresh_token = create_refresh_token(identity=user.id)
                        user.refresh_token = refresh_token
                        self.session.commit()
                        return {
                            'access_token': create_access_token(identity=user_identity),
                            'refresh_token': create_refresh_token(identity=user.id)
                        }, 200
                    except Exception as e:
                        return ErrorHandler().get_error(500, 'Error to process your login.')
                else:
                    return ErrorHandler().get_error(401, 'Invalid credencials.')
            else:
                return ErrorHandler().get_error(401, 'Invalid credencials.')
        else:
            return ErrorHandler().get_error(400, 'Insufficient credentials.')


    def _refresh(self):

        try:
            access = decode_token('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1OTA0NTI1MjAsIm5iZiI6MTU5MDQ1MjUyMCwianRpIjoiZmE4MzQ4MDUtODg5Ni00OGJhLWI3Y2MtZTZlNjg2MTQ5MTJjIiwiZXhwIjoxNTkwNDUyNTgwLCJpZGVudGl0eSI6IndlbGlzb24iLCJ0eXBlIjoicmVmcmVzaCJ9.vw9G0m6AMpTzeDqD_t8PbH9S-wEki9k4ZfRrRvoLyj0')

            if 'identity' in access:
                return {
                    'access_token': create_access_token(identity=access['identity'])
                }, 200

        except Exception as e:
            
            return 'sem acesso'

        
