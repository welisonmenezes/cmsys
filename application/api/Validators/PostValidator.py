from .ValidatorBase import ValidatorBase
from Models import Session, Post

class PostValidator(ValidatorBase):
    """Configures the Post validator to the parent class applies the validators correctly."""

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
            'title': {
                'key_required': True,
                'field_required': True,
                'max_length': 255,
                'min_length': 1
            },
            'description': {
                'key_required': True,
                'max_length': 65535
            },
            'status': {
                'key_required': True,
                'field_required': True,
                'max_length': 15,
                'min_length': 1,
                'valid_values': ['pending', 'publish', 'draft', 'trash', 'private']
            },
            'is_protected': {
                'key_required': True,
                'field_required': True,
                'is_boolean': True
            },
            'has_comments': {
                'key_required': True,
                'field_required': True,
                'is_boolean': True
            },
            'publish_on': {
                'key_required': True,
                'max_length': 19,
                'is_datetime': True
            },
            'expire_on': {
                'key_required': True,
                'max_length': 19,
                'is_datetime': True,
                'compare_dates': 'publish_on'
            },
            'parent_id': {
                'is_integer': True
            },
            'post_type_id': {
                'key_required': True,
                'field_required': True,
                'is_integer': True
            },
            'language_id': {
                'key_required': True,
                'field_required': True,
                'is_integer': True
            },
            'user_id': {
                'key_required': True,
                'field_required': True,
                'is_integer': True
            }
        }

        self.errors = []
        self.has_error = False
        self.complete_key_list = True
        self.model = Post
        self.session = Session
