from .ControllerBase import ControllerBase
from Repositories import SocialRepository

class SocialController(ControllerBase):
    """This flask_restful API's Resource works like a controller to SocialRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(SocialController, self).__init__()
        self.parser.add_argument('name')
        self.parser.add_argument('origin')
        self.parser.add_argument('user_id')
        self.parser.add_argument('get_user')
        self.parser.add_argument('get_configuration')
        self.args = self.parser.parse_args()
        self.repo = SocialRepository()