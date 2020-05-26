from flask import request
from flask_jwt_extended import decode_token
from ErrorHandlers import NotAuthorizedError, BadRequestError, NotFoundError
from Decorators import SingletonDecorator
from Models import Session, Blacklist, User

class AuthUtils():

    def __init__(self):

        self.session = Session()


    def get_authorized_passport(self, from_where='Authorization', verify_blacklist=True, token_key='token'):
        """Get the authorized user based on the given token. This can come from Authorization or Request."""

        token: None

        if from_where == 'Authorization':
            token = request.headers.get('Authorization')

        elif from_where == 'Request':
            data = request.get_json()
            if token_key in data and data[token_key] != '':
                token = data[token_key]

        else:
            raise BadRequestError('Invalid resource origin.')

        if token:

            if verify_blacklist:
                blacklist = self.session.query(Blacklist.id).filter_by(value=token).first()
                if blacklist:
                    raise NotAuthorizedError('Token revoked.')

            try:
                access = decode_token(token)
                if 'identity' in access:
                    identity = access['identity']
                    if 'id' in identity and 'login' in identity and 'role' in identity:
                        user = self.session.query(User).filter_by(login=identity['login']).first()
                        if user:
                            return {
                                'user': user,
                                'access': access
                            }
                        else:
                            raise NotFoundError('No user found.')
                    else:
                        raise BadRequestError('Invalid identity.')
                else:
                    raise BadRequestError('Invalid Token.')
            except Exception as e:
                raise NotAuthorizedError('Token already expired.')
        else:
            raise NotAuthorizedError('No Token send.')

