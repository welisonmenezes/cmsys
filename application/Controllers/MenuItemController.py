from .ControllerBase import ControllerBase
from Repositories import MenuItemRepository
from Utils import Helper

class MenuItemController(ControllerBase):
    """This flask_restful API's Resource works like a controller to MenuItemRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(MenuItemController, self).__init__()
        self.args = Helper().add_request_data(self.parser, [
            'type', 'behavior', 'url', 'title', 'parent_id', 'menu_id', 'get_menu', 'get_parent', 'get_children'])
        self.repo = MenuItemRepository()