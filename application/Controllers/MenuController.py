from .ControllerBase import ControllerBase
from Repositories import MenuRepository
from Utils import Helper

class MenuController(ControllerBase):
    """This flask_restful API's Resource works like a controller to MenuRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(MenuController, self).__init__()
        self.args = Helper().add_request_data(self.parser, ['s', 'language_id', 'get_language', 'get_sectors', 'get_items'])
        self.repo = MenuRepository()