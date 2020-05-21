from .ControllerBase import ControllerBase
from Repositories import FieldContentRepository

class FieldContentController(ControllerBase):
    """This flask_restful API's Resource works like a controller to FieldContentRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(FieldContentController, self).__init__()
        self.parser.add_argument('content')
        self.parser.add_argument('field_id')
        self.parser.add_argument('grouper_id')
        self.parser.add_argument('post_id')
        self.args = self.parser.parse_args()
        self.repo = FieldContentRepository()