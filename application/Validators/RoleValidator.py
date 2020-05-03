from .ValidatorBase import ValidatorBase

class RoleValidator(ValidatorBase):

    def __init__(self, obj_data):

        self.request = obj_data

        self.validate_config = {
            'name': {
                'key_required': True,
                'field_required': True,
                'max_length': 100,
                'min_length': 1
            },
            'description': {
                'key_required': False,
                'field_required': False,
                'max_length': 255
            },
            'can_access_admin': {
                'key_required': True,
                'field_required': True,
                'is_boolean': True
            }
        }

        self.errors = []
        self.has_error = False
        self.complete_key_list = True
