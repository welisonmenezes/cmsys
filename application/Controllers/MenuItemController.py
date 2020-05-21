from .ControllerBase import ControllerBase
from Repositories import MenuItemRepository

class MenuItemController(ControllerBase):
    """This flask_restful API's Resource works like a controller to MenuItemRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(MenuItemController, self).__init__()
        self.parser.add_argument('type')
        self.parser.add_argument('behavior')
        self.parser.add_argument('url')
        self.parser.add_argument('title')
        self.parser.add_argument('parent_id')
        self.parser.add_argument('menu_id')
        self.parser.add_argument('get_menu')
        self.parser.add_argument('get_parent')
        self.parser.add_argument('get_children')
        self.args = self.parser.parse_args()
        self.repo = MenuItemRepository()