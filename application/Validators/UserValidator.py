from .ValidatorBase import ValidatorBase
from Models import Session, User

class UserValidator(ValidatorBase):
    """Configures the User validator to the parent class applies the validators correctly."""

    def __init__(self, obj_data):
        """Gets the object data that will be validated and initializes the configurations."""

        self.request = obj_data

        self.validate_config = {
            'login': {
                'key_required': True,
                'field_required': True,
                'max_length': 100,
                'min_length': 1,
                'is_unique': True
            },
            'password': {
                'key_required': True,
                'field_required': True,
                'max_length': 255,
                'min_length': 6
            },
            'nickname': {
                'key_required': True,
                'max_length': 100
            },
            'first_name': {
                'key_required': True,
                'max_length': 100
            },
            'last_name': {
                'key_required': True,
                'max_length': 100
            },
            'email': {
                'key_required': True,
                'field_required': True,
                'max_length': 100,
                'min_length': 1
            },
            'status': {
                'key_required': True,
                'field_required': True,
                'max_length': 15,
                'min_length': 1
            },
            'role_id': {
                'key_required': True,
                'field_required': True,
                'min_length': 1,
                'is_integer': True
            },
            'avatar_id': {
                'is_integer': True
            },
            'page_id': {
                'is_integer': True
            }
        }

        self.errors = []
        self.has_error = False
        self.complete_key_list = True
        self.model = User
        self.session = Session
