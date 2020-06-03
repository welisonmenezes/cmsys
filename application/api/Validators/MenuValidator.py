from .ValidatorBase import ValidatorBase
from Models import Session, Menu

class MenuValidator(ValidatorBase):
    """Configures the Menu validator to the parent class applies the validators correctly."""

    def __init__(self, obj_data):
        """Gets the object data that will be validated and initializes the configurations."""

        self.request = obj_data

        self.validate_config = {
            'name': {
                'key_required': True,
                'field_required': True,
                'max_length': 100,
                'min_length': 1,
                'is_unique': True
            },
            'order': {
                'key_required': True,
                'field_required': True,
                'min_length': 1,
                'is_integer': True
            },
            'description': {
                'key_required': True,
                'max_length': 255,
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
        self.model = Menu
        self.session = Session
