from .ControllerBase import ControllerBase
from Repositories import SectorRepository
from Utils import Helper

class SectorController(ControllerBase):
    """This flask_restful API's Resource works like a controller to SectorRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(SectorController, self).__init__()
        self.args = Helper().add_request_data(self.parser, ['s', 'get_menus'])
        self.repo = SectorRepository(session=self.session)