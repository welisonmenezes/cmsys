from .ControllerBase import ControllerBase
from Repositories import LanguageRepository

class LanguageController(ControllerBase):
    """This flask_restful API's Resource works like a controller to LanguageRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(LanguageController, self).__init__()
        self.parser.add_argument('name')
        self.parser.add_argument('code')
        self.parser.add_argument('status')
        self.args = self.parser.parse_args()
        self.repo = LanguageRepository()