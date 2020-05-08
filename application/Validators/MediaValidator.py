from .ValidatorBase import ValidatorBase
from Models import Session, Media

class MediaValidator(ValidatorBase):

    def __init__(self, obj_data):

        self.request = obj_data

        self.validate_config = {
            'name': {
                'key_required': True,
                'field_required': True,
                'max_length': 100,
                'min_length': 1,
                'is_unique': True
            },
            'description': {
                'key_required': True,
                'max_length': 255
            },
            'extension': {
                'key_required': True,
                'field_required': True,
                'max_length': 4,
                'min_length': 1,
                'valid_file_extension': True
            },
            'file': {
                'key_required': True,
                'field_required_only_post': True,
                'is_file': True,
                'max_file_size': True,
                'valid_file_type': True,
            },
            'origin': {
                'key_required': True,
                'field_required': True,
                'max_length': 50,
                'min_length': 1
            },
            'user_id': {
                'key_required': True,
                'field_required': True,
                'is_integer': True
            }
        }

        self.errors = []
        self.has_error = False
        self.complete_key_list = True
        self.model = Media
        self.session = Session