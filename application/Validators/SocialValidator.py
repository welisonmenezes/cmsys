from .ValidatorBase import ValidatorBase

class SocialValidator(ValidatorBase):

    def __init__(self, obj_data):

        self.request = obj_data

        self.validate_config = {
            'name': {
                'key_required': True,
                'field_required': True,
                'max_length': 100,
                'min_length': 1
            },
            'url': {
                'key_required': True,
                'field_required': True,
                'max_length': 255,
                'min_length': 1
            },
            'target': {
                'key_required': True,
                'max_length': 15
            },
            'description': {
                'key_required': True,
                'max_length': 255
            },
            'origin': {
                'key_required': True,
                'field_required': True,
                'max_length': 50,
                'min_length': 1
            },
            'configuration_id': {
                'is_integer': True
            },
            'user_id': {
                'is_integer': True
            },
        }

        self.errors = []
        self.has_error = False
        self.complete_key_list = True
        self.model = None
        self.session = None
