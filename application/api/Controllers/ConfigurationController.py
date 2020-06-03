from .ControllerBase import ControllerBase
from Repositories import ConfigurationRepository
from Utils import Helper

class ConfigurationController(ControllerBase):
    """This flask_restful API's Resource works like a controller to ConfigurationRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(ConfigurationController, self).__init__()
        self.args = Helper().add_request_data(self.parser, ['s', 'has_comments', 'language_id', 'get_language', 'get_socials'])
        self.repo = ConfigurationRepository(session=self.session)