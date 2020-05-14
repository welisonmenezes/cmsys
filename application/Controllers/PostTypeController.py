from .ControllerBase import ControllerBase
from Repositories import PostTypeRepository

class PostTypeController(ControllerBase):
    """This flask_restful API's Resource works like a controller to PostTypeRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(PostTypeController, self).__init__()
        self.repo = PostTypeRepository()
        

    def get(self, id=None):
        """Rewrite ControllerBase get method to apply customizations to the get http verb responder."""

        self.parser.add_argument('name')
        self.parser.add_argument('type')
        self.parser.add_argument('get_template')
        self.args = self.parser.parse_args()

        return self.repo.get_by_id(id, self.args) if id else self.repo.get(self.args)