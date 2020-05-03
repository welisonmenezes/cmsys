from .ValidatorBase import ValidatorBase

class VariableValidator(ValidatorBase):

    def __init__(self, obj_data):

        self.request = obj_data

        self.validate_config = {
            'key': {
                'key_required': True,
                'field_required': True,
                'max_length': 255,
                'min_length': 1
            },
            'value': {
                'key_required': True,
                'field_required': True,
                'min_length': 1
            }
        }

        self.errors = []
        self.has_error = False
