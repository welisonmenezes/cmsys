from .ControllerBase import ControllerBase
from Repositories import BlacklistRepository

class BlacklistController(ControllerBase):
    """This flask_restful API's Resource works like a controller to BlacklistRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(BlacklistController, self).__init__()
        self.parser.add_argument('value')
        self.parser.add_argument('type')
        self.parser.add_argument('target')
        self.args = self.parser.parse_args()
        self.repo = BlacklistRepository()