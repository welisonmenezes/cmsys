from .ValidatorBase import ValidatorBase
from Models import Session, Variable

class VariableValidator(ValidatorBase):
    """Configures the Variable validator to the parent class applies the validators correctly."""

    def __init__(self, obj_data):
        """Gets the object data that will be validated and initializes the configurations."""

        self.request = obj_data

        self.validate_config = {
            'key': {
                'key_required': True,
                'field_required': True,
                'max_length': 255,
                'min_length': 1,
                'is_unique': True
            },
            'value': {
                'key_required': True,
                'field_required': True,
                'min_length': 1,
                'max_length': 4294967295
            }
        }

        self.errors = []
        self.has_error = False
        self.complete_key_list = True
        self.model = Variable
        self.session = Session
