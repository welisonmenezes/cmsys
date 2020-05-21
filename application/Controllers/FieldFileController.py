from .ControllerBase import ControllerBase
from Repositories import FieldFileRepository

class FieldFileController(ControllerBase):
    """This flask_restful API's Resource works like a controller to FieldFileRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(FieldFileController, self).__init__()
        self.parser.add_argument('field_id')
        self.parser.add_argument('media_id')
        self.parser.add_argument('grouper_id')
        self.parser.add_argument('post_id')
        self.args = self.parser.parse_args()
        self.repo = FieldFileRepository()