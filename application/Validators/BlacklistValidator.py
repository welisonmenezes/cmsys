from .ValidatorBase import ValidatorBase

class BlacklistValidator(ValidatorBase):

    def __init__(self, obj_data):

        self.request = obj_data

        self.validate_config = {
            'type': {
                'key_required': True,
                'field_required': True,
                'max_length': 50,
                'min_length': 1
            },
            'value': {
                'key_required': True,
                'field_required': True,
                'min_length': 1
            },
            'target': {
                'key_required': True,
                'field_required': True,
                'max_length': 100,
                'min_length': 1
            }
        }

        self.errors = []
        self.has_error = False
        self.complete_key_list = True
