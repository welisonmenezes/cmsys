from .ControllerBase import ControllerBase
from Repositories import NestRepository
from Utils import Helper

class NestController(ControllerBase):
    """This flask_restful API's Resource works like a controller to NestRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(NestController, self).__init__()
        self.args = Helper().add_request_data(self.parser, ['s', 'post_id', 'post_type_id', 'get_post', 'get_post_type'])
        self.repo = NestRepository()