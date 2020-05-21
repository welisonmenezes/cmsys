from .ControllerBase import ControllerBase
from Repositories import BlacklistRepository
from Utils import Helper

class BlacklistController(ControllerBase):
    """This flask_restful API's Resource works like a controller to BlacklistRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(BlacklistController, self).__init__()
        self.args = Helper().add_request_data(self.parser, ['value', 'type', 'target'])
        print(self.args)
        self.repo = BlacklistRepository()