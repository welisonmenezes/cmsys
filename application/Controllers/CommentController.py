from .ControllerBase import ControllerBase
from Repositories import CommentRepository

class CommentController(ControllerBase):
    """This flask_restful API's Resource works like a controller to CommentRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(CommentController, self).__init__()
        self.repo = CommentRepository()
        

    def get(self, id=None):
        """Rewrite ControllerBase get method to apply customizations to the get http verb responder."""

        self.parser.add_argument('comment')
        self.parser.add_argument('status')
        self.parser.add_argument('origin_ip')
        self.parser.add_argument('origin_agent')
        self.parser.add_argument('created')
        self.parser.add_argument('parent_id')
        self.parser.add_argument('user_id')
        self.parser.add_argument('post_id')
        self.parser.add_argument('language_id')
        self.parser.add_argument('get_user')
        self.parser.add_argument('get_language')
        self.parser.add_argument('get_post')
        self.parser.add_argument('get_parent')
        self.parser.add_argument('get_children')
        self.args = self.parser.parse_args()

        return self.repo.get_by_id(id, self.args) if id else self.repo.get(self.args)