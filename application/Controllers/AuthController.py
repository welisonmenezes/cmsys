from flask import jsonify, request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from app import bcrypt
from ErrorHandlers import ErrorHandler
from Models import Session, User, Blacklist

class AuthController(Resource):
    """This flask_restful API's Resource works like a controller to AuthRepository."""

    def __init__(self):
        self.session = Session()


    def post(self):
        """Sets the available endpoints to deal with Tokens."""

        if str(request.url_rule) == '/api/get-token':
            return self._get_token()
        elif str(request.url_rule) == '/api/refresh-token':
            return self._refresh_token()
        elif str(request.url_rule) == '/api/revoke-token':
            return self._revoke_token()
        elif str(request.url_rule) == '/api/test-token':
            return self._test_token()
        
        return ErrorHandler().get_error(405, 'Method not allowed.')


    def _get_token(self):
        """Gets the Token and Refresh Token to valid user."""

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


    def _refresh_token(self):
        """Refreshes the Token by the given Refresh Token only if it is valid yet."""

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
                            return ErrorHandler().get_error(404, 'No user found.')
                    else:
                        return ErrorHandler().get_error(400, 'Invalid identity.')
                else:
                    return ErrorHandler().get_error(400, 'Invalid Refresh Token.')
            except Exception as e:
                return ErrorHandler().get_error(401, 'Refresh Token expired.')
        else:
            return ErrorHandler().get_error(400, 'No Refresh Token send.')


    def _revoke_token(self):
        """Revokes the given Token by adding it into a blacklist and empties the user Refresh Token."""

        data = request.get_json()
        if 'token' in data and data['token'] != '':
            try:
                access = decode_token(data['token'])
                if 'identity' in access:
                    identity = access['identity']
                    if 'id' in identity and 'login' in identity and 'role' in identity:
                        user = self.session.query(User).filter_by(login=identity['login']).first()
                        if user:
                            if not user.refresh_token or user.refresh_token == '':
                                return ErrorHandler().get_error(401, 'Token already revoked.')
                            try:
                                user.refresh_token = None
                                blacklist = Blacklist(
                                    type = 'token',
                                    value = data['token'],
                                    target = 'auth'
                                )
                                self.session.add(blacklist)
                                self.session.commit()
                                return {'message': 'Token revoked successfully.'}, 200
                            except Exception as e:
                                self.session.rollback()
                                return ErrorHandler().get_error(500, 'Error to process the token revoking.')
                        else:
                            return ErrorHandler().get_error(404, 'No user found.')
                    else:
                        return ErrorHandler().get_error(400, 'Invalid identity.')
                else:
                    return ErrorHandler().get_error(400, 'Invalid Token.')
            except Exception as e:
                return ErrorHandler().get_error(401, 'Token already expired.')
        else:
            return ErrorHandler().get_error(400, 'No Token send.')


    def _test_token(self):
        """Just a endpoint to test the given Token sent by request header into the Authorization key."""

        token = request.headers.get('Authorization')
        if token:
            blacklist = self.session.query(Blacklist.id).filter_by(value=token).first()
            if blacklist:
                return ErrorHandler().get_error(401, 'Token revoked.')
            else:
                try:
                    access = decode_token(token)
                    if 'identity' in access:
                        identity = access['identity']
                        if 'id' in identity and 'login' in identity and 'role' in identity:
                            user = self.session.query(User).filter_by(login=identity['login']).first()
                            if user:
                                return {'message': 'Your token is valid.'}, 200
                            else:
                                return ErrorHandler().get_error(404, 'No user found.')
                        else:
                            return ErrorHandler().get_error(400, 'Invalid identity.')
                    else:
                        return ErrorHandler().get_error(400, 'Invalid Token.')
                except Exception as e:
                    return ErrorHandler().get_error(401, 'Token already expired.')
        else:
            return ErrorHandler().get_error(401, 'No Token send.')