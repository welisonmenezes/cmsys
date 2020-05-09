from app import app_config
from Decorators import SingletonDecorator

@SingletonDecorator
class Checker():

    def can_be_integer(self, element):
        try:
            int(element)
            return True
        except ValueError:
            return False


    def is_image_type(self, mimetype):
        image_types = app_config['IMAGE_MIMETYPES'].keys()
        return True if mimetype in image_types else False