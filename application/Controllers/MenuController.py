from .ControllerBase import ControllerBase
from Repositories import MenuRepository

class MenuController(ControllerBase):
    """This flask_restful API's Resource works like a controller to MenuRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(MenuController, self).__init__()
        self.parser.add_argument('s')
        self.parser.add_argument('language_id')
        self.parser.add_argument('get_language')
        self.parser.add_argument('get_sectors')
        self.parser.add_argument('get_items')
        self.args = self.parser.parse_args()
        self.repo = MenuRepository()