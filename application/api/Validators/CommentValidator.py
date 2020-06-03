from .ValidatorBase import ValidatorBase

class CommentValidator(ValidatorBase):
    """Configures the Comment validator to the parent class applies the validators correctly."""

    def __init__(self, obj_data):
        """Gets the object data that will be validated and initializes the configurations."""

        self.request = obj_data

        self.validate_config = {
            'comment': {
                'key_required': True,
                'field_required': True,
                'min_length': 1,
                'max_length': 65535
            },
            'status': {
                'key_required': True,
                'field_required': True,
                'min_length': 1,
                'max_length': 15
            },
            'origin_ip': {
                'key_required': True,
                'field_required': True,
                'max_length': 100,
                'min_length': 1
            },
            'origin_agent': {
                'key_required': True,
                'field_required': True,
                'max_length': 255,
                'min_length': 1
            },
            'parent_id': {
                'is_integer': True
            },
            'user_id': {
                'key_required': True,
                'field_required': True,
                'is_integer': True
            },
            'post_id': {
                'key_required': True,
                'field_required': True,
                'is_integer': True
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
