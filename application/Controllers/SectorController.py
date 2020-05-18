from .ControllerBase import ControllerBase
from Repositories import SectorRepository

class SectorController(ControllerBase):
    """This flask_restful API's Resource works like a controller to SectorRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(SectorController, self).__init__()
        self.repo = SectorRepository()
        

    def get(self, id=None):
        """Rewrite ControllerBase get method to apply customizations to the get http verb responder."""

        self.parser.add_argument('s')
        self.parser.add_argument('get_menus')
        self.args = self.parser.parse_args()

        return self.repo.get_by_id(id, self.args) if id else self.repo.get(self.args)