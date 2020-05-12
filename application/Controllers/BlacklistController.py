from .ControllerBase import ControllerBase
from Repositories import BlacklistRepository

class BlacklistController(ControllerBase):
    """This flask_restful API's Resource works like a controller to BlacklistRepository"""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved"""

        super(BlacklistController, self).__init__()
        self.repo = BlacklistRepository()
        

    def get(self, id=None):
        """Rewrite ControllerBase get method to apply customizations to the get http verb responder"""

        self.parser.add_argument('value')
        self.parser.add_argument('type')
        self.parser.add_argument('target')
        self.args = self.parser.parse_args()

        return self.repo.get_by_id(id) if id else self.repo.get(self.args)