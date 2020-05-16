from .ControllerBase import ControllerBase
from Repositories import UserRepository

class UserController(ControllerBase):
    """This flask_restful API's Resource works like a controller to UserRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(UserController, self).__init__()
        self.repo = UserRepository()
        

    def get(self, id=None):
        """Rewrite ControllerBase get method to apply customizations to the get http verb responder."""

        self.parser.add_argument('s')
        self.parser.add_argument('email')
        self.parser.add_argument('registered')
        self.parser.add_argument('status')
        self.parser.add_argument('role_id')
        self.parser.add_argument('get_role')
        self.parser.add_argument('get_socials')
        self.parser.add_argument('get_medias')
        self.parser.add_argument('get_page')
        self.parser.add_argument('get_avatar')
        self.parser.add_argument('admin_new_owner')
        self.args = self.parser.parse_args()

        return self.repo.get_by_id(id, self.args) if id else self.repo.get(self.args)