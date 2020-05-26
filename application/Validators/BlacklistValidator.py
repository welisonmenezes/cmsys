from .ValidatorBase import ValidatorBase

class BlacklistValidator(ValidatorBase):
    """Configures the Blacklist validator to the parent class applies the validators correctly."""

    def __init__(self, obj_data):
        """Gets the object data that will be validated and initializes the configurations."""

        self.request = obj_data

        self.validate_config = {
            'type': {
                'key_required': True,
                'field_required': True,
                'max_length': 50,
                'min_length': 1,
                'valid_values': ['email', 'ip', 'domain', 'token']
            },
            'value': {
                'key_required': True,
                'field_required': True,
                'min_length': 1,
                'max_length': 65535
            },
            'target': {
                'key_required': True,
                'field_required': True,
                'max_length': 100,
                'min_length': 1,
                'valid_values': ['comment', 'login', 'private-access', 'public-access', 'auth']
            }
        }

        self.errors = []
        self.has_error = False
        self.complete_key_list = True
        self.model = None
        self.session = None
