from .ValidatorBase import ValidatorBase

class MenuItemValidator(ValidatorBase):
    """Configures the MenuItem validator to the parent class applies the validators correctly."""

    def __init__(self, obj_data):
        """Gets the object data that will be validated and initializes the configurations."""

        self.request = obj_data

        self.validate_config = {
            'type': {
                'key_required': True,
                'field_required': True,
                'max_length': 50,
                'min_length': 1,
                'valid_values': ['anchor', 'post', 'term', 'external']
            },
            'behavior': {
                'key_required': True,
                'field_required': True,
                'max_length': 50,
                'min_length': 1,
                'valid_values': ['_blank', '_self', '_parent', '_top']
            },
            'url': {
                'key_required': True,
                'max_length': 255
            },
            'target_id': {
                'is_integer': True
            },
            'title': {
                'key_required': True,
                'field_required': True,
                'max_length': 255,
                'min_length': 1
            },
            'order': {
                'key_required': True,
                'field_required': True,
                'min_length': 1,
                'is_integer': True
            },
            'parent_id': {
                'is_integer': True
            },
            'menu_id': {
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
