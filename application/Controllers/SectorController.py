from .ControllerBase import ControllerBase
from Repositories import SectorRepository

class SectorController(ControllerBase):
    """This flask_restful API's Resource works like a controller to SectorRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(SectorController, self).__init__()
        self.parser.add_argument('s')
        self.parser.add_argument('get_menus')
        self.args = self.parser.parse_args()
        self.repo = SectorRepository()