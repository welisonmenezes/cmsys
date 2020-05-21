from .ControllerBase import ControllerBase
from Repositories import PostTypeRepository

class PostTypeController(ControllerBase):
    """This flask_restful API's Resource works like a controller to PostTypeRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(PostTypeController, self).__init__()
        self.parser.add_argument('name')
        self.parser.add_argument('type')
        self.parser.add_argument('get_template')
        self.parser.add_argument('get_nests')
        self.args = self.parser.parse_args()
        self.repo = PostTypeRepository()