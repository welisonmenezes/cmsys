from .ValidatorBase import ValidatorBase
from Models import Session, Language

class LanguageValidator(ValidatorBase):
    """Configures the Language validator to the parent class applies the validators correctly."""

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
            'code': {
                'key_required': True,
                'field_required': True,
                'max_length': 10,
                'min_length': 1,
                'is_unique': True
            },
            'status': {
                'key_required': True,
                'field_required': True,
                'max_length': 15,
                'min_length': 1
            },
            'datetime_format': {
                'max_length': 100
            }
        }

        self.errors = []
        self.has_error = False
        self.complete_key_list = True
        self.model = Language
        self.session = Session
