from .ValidatorBase import ValidatorBase

class VariableValidator(ValidatorBase):

    def __init__(self, obj_data):

        self.request = obj_data

        self.required_keys = [
            'key',
            'value'
        ]

        self.required_fields = [
            'key'
        ]

        self.errors = []
        self.has_error = False
