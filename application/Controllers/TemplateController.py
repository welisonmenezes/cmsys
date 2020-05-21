from .ControllerBase import ControllerBase
from Repositories import TemplateRepository

class TemplateController(ControllerBase):
    """This flask_restful API's Resource works like a controller to TemplateRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(TemplateController, self).__init__()
        self.parser.add_argument('name')
        self.parser.add_argument('s')
        self.parser.add_argument('get_post_types')
        self.args = self.parser.parse_args()
        self.repo = TemplateRepository()