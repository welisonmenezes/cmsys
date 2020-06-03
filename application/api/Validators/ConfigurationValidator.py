from .ValidatorBase import ValidatorBase

class ConfigurationValidator(ValidatorBase):
    """Configures the Configuration validator to the parent class applies the validators correctly."""

    def __init__(self, obj_data):
        """Gets the object data that will be validated and initializes the configurations."""

        self.request = obj_data

        self.validate_config = {
            'title': {
                'key_required': True,
                'field_required': True,
                'max_length': 255,
                'min_length': 1
            },
            'description': {
                'key_required': True,
                'max_length': 255,
            },
            'has_comments': {
                'key_required': True,
                'field_required': True,
                'is_boolean': True
            },
            'email': {
                'key_required': True,
                'max_length': 100,
            },
            'language_id': {
                'key_required': True,
                'field_required': True,
                'is_integer': True
            }
        }

        self.errors = []
        self.has_error = False
        self.complete_key_list = True
        self.model = None
        self.session = None
