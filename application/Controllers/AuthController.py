from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from app import bcrypt
from ErrorHandlers import ErrorHandler, NotFoundError, NotAuthorizedError, BadRequestError
from Models import Session, User, Blacklist, UserSchema
from Auth import AuthUtils

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

        def fn():
            passport = AuthUtils().get_authorized_passport(from_where='Request', verify_blacklist=False, token_key='refresh_token')
            print(passport)
            data = request.get_json()
            if passport['user'].refresh_token == data['refresh_token']:
                try:
                    token = create_access_token(identity=passport['access']['identity'])
                    refresh_token = create_refresh_token(identity=passport['access']['identity'])
                    passport['user'].refresh_token = refresh_token
                    self.session.commit()
                    return {
                        'access_token': token,
                        'refresh_token': refresh_token
                    }, 200
                except Exception as e:
                    print(e)
                    return ErrorHandler().get_error(500, 'Error to process the token refreshing.')
            else:
                return ErrorHandler().get_error(401, 'The given Refresh Token is not available.')
        return self.run_if_not_raise(fn)


    def _revoke_token(self):
        """Revokes the given Token by adding it into a blacklist and empties the user Refresh Token."""

        def fn():
            passport = AuthUtils().get_authorized_passport(from_where='Request', verify_blacklist=True)
            if not passport['user'].refresh_token or passport['user'].refresh_token == '':
                return ErrorHandler().get_error(401, 'Token already revoked.')
            try:
                data = request.get_json()
                passport['user'].refresh_token = None
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
        return self.run_if_not_raise(fn)


    def _test_token(self):
        """Just a endpoint to test the given Token sent by request header into the Authorization key."""

        def fn():
            passport = AuthUtils().get_authorized_passport()
            schema = UserSchema(many=False, exclude=('password', 'refresh_token', 'medias', 'socials'))
            return {
                'user': schema.dump(passport['user']),
                'access': passport['access']
            }, 200
        return self.run_if_not_raise(fn)


    def run_if_not_raise(self, fn):
        """Catch exception if it occurs, if not, execute the given function."""

        try:
            return fn()
        except NotAuthorizedError as e:
            return ErrorHandler().get_error(401, str(e))
        except BadRequestError as e:
            return ErrorHandler().get_error(400, str(e))
        except NotFoundError as e:
            return ErrorHandler().get_error(404, str(e))
        except Exception as e:
            return ErrorHandler().get_error(500, str(e))