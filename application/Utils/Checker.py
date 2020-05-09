from app import app_config

class Checker():

    @staticmethod
    def can_be_integer(element):
        try:
            int(element)
            return True
        except ValueError:
            return False


    @staticmethod
    def is_image_type(mimetype):
        image_types = app_config['IMAGE_MIMETYPES'].keys()
        if (mimetype in image_types):
            return True
        else:
            return False