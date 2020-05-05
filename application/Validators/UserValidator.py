from .ValidatorBase import ValidatorBase

class UserValidator(ValidatorBase):

    def __init__(self, obj_data):

        self.request = obj_data

        self.validate_config = {
            'login': {
                'key_required': True,
                'field_required': True,
                'max_length': 100,
                'min_length': 1
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
                'key_required': True,
                'is_integer': True
            },
            'page_id': {
                'key_required': True,
                'is_integer': True
            }
        }

        self.errors = []
        self.has_error = False
        self.complete_key_list = True
        self.model = None
        self.session = None
