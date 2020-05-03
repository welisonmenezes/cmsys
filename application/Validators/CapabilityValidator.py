from .ValidatorBase import ValidatorBase

class CapabilityValidator(ValidatorBase):

    def __init__(self, obj_data):

        self.request = obj_data

        self.validate_config = {
            'description': {
                'key_required': True,
                'field_required': True,
                'max_length': 255,
                'min_length': 1
            },
            'type': {
                'key_required': True,
                'field_required': True,
                'max_length': 50,
                'min_length': 1
            },
            'target_id': {
                'key_required': True,
                'field_required': True,
                'min_length': 1,
                'is_integer': True
            },
            'can_write': {
                'key_required': True,
                'field_required': True,
                'is_boolean': True
            },
            'can_read': {
                'key_required': True,
                'field_required': True,
                'is_boolean': True
            },
            'can_delete': {
                'key_required': True,
                'field_required': True,
                'is_boolean': True
            }
        }

        self.errors = []
        self.has_error = False
        self.complete_key_list = True
        self.model = None
        self.session = None
