from .ControllerBase import ControllerBase
from Repositories import SocialRepository
from Utils import Helper

class SocialController(ControllerBase):
    """This flask_restful API's Resource works like a controller to SocialRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(SocialController, self).__init__()
        self.args = Helper().add_request_data(self.parser, ['name', 'origin', 'user_id', 'get_user', 'get_configuration'])
        self.repo = SocialRepository()