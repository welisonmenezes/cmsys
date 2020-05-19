from .ControllerBase import ControllerBase
from Repositories import FieldRepository

class FieldController(ControllerBase):
    """This flask_restful API's Resource works like a controller to FieldRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(FieldController, self).__init__()
        self.repo = FieldRepository()
        

    def get(self, id=None):
        """Rewrite ControllerBase get method to apply customizations to the get http verb responder."""

        self.parser.add_argument('s')
        self.parser.add_argument('type')
        self.parser.add_argument('grouper_id')
        self.parser.add_argument('post_id')
        self.parser.add_argument('get_post')
        self.parser.add_argument('get_grouper')
        self.args = self.parser.parse_args()

        return self.repo.get_by_id(id, self.args) if id else self.repo.get(self.args)