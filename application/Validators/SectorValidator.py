from .ValidatorBase import ValidatorBase
from Models import Session, Sector

class SectorValidator(ValidatorBase):
    """Configures the Sector validator to the parent class applies the validators correctly."""

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
            'description': {
                'key_required': True,
                'max_length': 255
            }
        }

        self.errors = []
        self.has_error = False
        self.complete_key_list = True
        self.model = Sector
        self.session = Session
