from .ControllerBase import ControllerBase
from Repositories import TemplateRepository
from Utils import Helper

class TemplateController(ControllerBase):
    """This flask_restful API's Resource works like a controller to TemplateRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(TemplateController, self).__init__()
        self.args = Helper().add_request_data(self.parser, ['name', 's', 'get_post_types'])
        self.repo = TemplateRepository()