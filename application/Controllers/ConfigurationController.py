from .ControllerBase import ControllerBase
from Repositories import ConfigurationRepository

class ConfigurationController(ControllerBase):
    """This flask_restful API's Resource works like a controller to ConfigurationRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(ConfigurationController, self).__init__()
        self.repo = ConfigurationRepository()
        

    def get(self, id=None):
        """Rewrite ControllerBase get method to apply customizations to the get http verb responder."""

        # self.parser.add_argument('value')
        # self.parser.add_argument('type')
        # self.parser.add_argument('target')
        self.args = self.parser.parse_args()

        return self.repo.get_by_id(id, self.args) if id else self.repo.get(self.args)