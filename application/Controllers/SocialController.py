from .ControllerBase import ControllerBase
from Repositories import SocialRepository

class SocialController(ControllerBase):
    """This flask_restful API's Resource works like a controller to SocialRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(SocialController, self).__init__()
        self.repo = SocialRepository()
        

    def get(self, id=None):
        """Rewrite ControllerBase get method to apply customizations to the get http verb responder."""

        self.parser.add_argument('name')
        self.parser.add_argument('origin')
        self.parser.add_argument('user_id')
        self.parser.add_argument('get_user')
        self.parser.add_argument('get_configuration')
        self.args = self.parser.parse_args()

        return self.repo.get_by_id(id, self.args) if id else self.repo.get(self.args)