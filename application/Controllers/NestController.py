from .ControllerBase import ControllerBase
from Repositories import NestRepository

class NestController(ControllerBase):
    """This flask_restful API's Resource works like a controller to NestRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(NestController, self).__init__()
        self.parser.add_argument('s')
        self.parser.add_argument('post_id')
        self.parser.add_argument('post_type_id')
        self.parser.add_argument('get_post')
        self.parser.add_argument('get_post_type')
        self.args = self.parser.parse_args()
        self.repo = NestRepository()