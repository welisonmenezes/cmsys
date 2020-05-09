from .ControllerBase import ControllerBase
from Repositories import MediaRepository
from Utils import ErrorHandler

class ImageController(ControllerBase):

    def __init__(self):
        self.repo = MediaRepository()
        super(ImageController, self).__init__()
        

    def get(self, id=None):
        if id:
            return self.repo.get_image_preview(id)

    
    def put(self, id=None):
        return ErrorHandler().get_error(405, 'Method not allowed.')


    def delete(self, id=None):
        return ErrorHandler().get_error(405, 'Method not allowed.')