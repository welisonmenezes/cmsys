from .ControllerBase import ControllerBase
from Repositories import LanguageRepository
from Utils import Helper

class LanguageController(ControllerBase):
    """This flask_restful API's Resource works like a controller to LanguageRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(LanguageController, self).__init__()
        self.args = Helper().add_request_data(self.parser, ['name', 'code', 'status'])
        self.repo = LanguageRepository()