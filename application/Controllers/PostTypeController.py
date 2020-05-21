from .ControllerBase import ControllerBase
from Repositories import PostTypeRepository
from Utils import Helper

class PostTypeController(ControllerBase):
    """This flask_restful API's Resource works like a controller to PostTypeRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(PostTypeController, self).__init__()
        self.args = Helper().add_request_data(self.parser, ['name', 'type', 'get_template', 'get_nests'])
        self.repo = PostTypeRepository()