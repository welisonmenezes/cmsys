from .ValidatorBase import ValidatorBase

class VariableValidator(ValidatorBase):

    def __init__(self, obj_data):

        self.request = obj_data

        self.validate_config = {
            'key': {
                'key_required': True,
                'field_required': True
            },
            'value': {
                'key_required': True,
                'field_required': True
            }
        }

        self.errors = []
        self.has_error = False
