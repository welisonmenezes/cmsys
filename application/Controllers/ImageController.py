from .ControllerBase import ControllerBase
from Repositories import MediaRepository
from Utils import ErrorHandler

class ImageController(ControllerBase):
    """This flask_restful API's Resource works like a controller to MediaRepository,
       but only implements the get_image_preview method of this repository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(ImageController, self).__init__()
        self.repo = MediaRepository()
        

    def get(self, id=None):
        """Rewrite ControllerBase get method to apply customizations to the get http verb responder."""

        if id:
            return self.repo.get_image_preview(id)

    
    def put(self, id=None):
        """Rewrite ControllerBase get method to apply customizations to the put http verb responder."""

        return ErrorHandler().get_error(405, 'Method not allowed.')


    def delete(self, id=None):
        """Rewrite ControllerBase get method to apply customizations to the delete http verb responder."""

        return ErrorHandler().get_error(405, 'Method not allowed.')