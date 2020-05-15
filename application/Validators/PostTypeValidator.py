from .ValidatorBase import ValidatorBase
from Models import Session, PostType

class PostTypeValidator(ValidatorBase):
    """Configures the PostType validator to the parent class applies the validators correctly."""

    def __init__(self, obj_data):
        """Gets the object data that will be validated and initializes the configurations."""

        self.request = obj_data

        self.validate_config = {
            'name': {
                'key_required': True,
                'field_required': True,
                'max_length': 255,
                'min_length': 1,
                'is_unique': True
            },
            'type': {
                'key_required': True,
                'field_required': True,
                'max_length': 50,
                'min_length': 1,
                'valid_values': ['user-profile', 'term-page', 'static-page', 'post-page', 'nested-page']
            },
            'template_id': {
                'is_integer': True
            }
        }

        self.errors = []
        self.has_error = False
        self.complete_key_list = True
        self.model = PostType
        self.session = Session
