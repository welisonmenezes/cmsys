from .ControllerBase import ControllerBase
from Repositories import MediaRepository

class ImageController(ControllerBase):

    def __init__(self):
        self.repo = MediaRepository()
        super(ImageController, self).__init__()
        

    def get(self, id=None):
        if id:
            return self.repo.get_image_preview(id)
