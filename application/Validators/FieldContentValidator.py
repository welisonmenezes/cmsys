from .ValidatorBase import ValidatorBase

class FieldContentValidator(ValidatorBase):
    """Configures the FieldContent validator to the parent class applies the validators correctly."""

    def __init__(self, obj_data):
        """Gets the object data that will be validated and initializes the configurations."""

        self.request = obj_data

        self.validate_config = {
            'content': {
                'key_required': True,
                'field_required': True,
                'min_length': 1
            },
            'field_id': {
                'key_required': True,
                'field_required': True,
                'is_integer': True
            },
            'grouper_id': {
                'key_required': True,
                'field_required': True,
                'is_integer': True
            },
            'post_id': {
                'key_required': True,
                'field_required': True,
                'is_integer': True
            },
        }

        self.errors = []
        self.has_error = False
        self.complete_key_list = True
        self.model = None
        self.session = None
