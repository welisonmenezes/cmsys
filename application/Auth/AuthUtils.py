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

    
    def verify_capabilities(self, capabilities, capability_type=None, permission=None, owner_id=None, user_id=None, new_owner_id=None):
        """Verify from the given capabilities if it matches with the given capability type and permission."""
    
        has_comparators = False
        if owner_id and user_id:
            has_comparators = True

        for capability in capabilities:
            if capability_type == getattr(capability, 'type') and getattr(capability, permission) == True and getattr(capability, 'only_themselves') == False:
                return True
            elif capability_type == getattr(capability, 'type') and getattr(capability, permission) == True and has_comparators:
                if new_owner_id and owner_id != new_owner_id:
                    raise NotAuthorizedError('You cannot change the owner ID of this element.')
                if owner_id != user_id:
                    raise NotAuthorizedError('You only can access your own element by this action.')
                return True
            
        raise NotAuthorizedError('Your profile does not has permission to access this resource.')