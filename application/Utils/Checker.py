from app import app_config
from Decorators import SingletonDecorator

@SingletonDecorator
class Checker():
    """Utility class to make boolean various verifications across the application"""

    def can_be_integer(self, value):
        """Checks if a string value can be converted to integer"""

        try:
            int(value)
            return True
        except ValueError:
            return False


    def is_image_type(self, mimetype):
        """Checks if a string mimetype exists into app config as valid image mimetype"""
        
        image_types = app_config['IMAGE_MIMETYPES'].keys()
        return True if mimetype in image_types else False