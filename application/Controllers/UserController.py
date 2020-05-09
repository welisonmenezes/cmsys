from .ControllerBase import ControllerBase
from Repositories import UserRepository

class UserController(ControllerBase):

    def __init__(self):
        self.repo = UserRepository()
        super(UserController, self).__init__()
        

    def get(self, id=None):
        self.parser.add_argument('name')
        self.parser.add_argument('email')
        self.parser.add_argument('registered')
        self.parser.add_argument('status')
        self.parser.add_argument('role_id')
        self.parser.add_argument('get_role')
        self.parser.add_argument('get_socials')
        self.args = self.parser.parse_args()

        return self.repo.get_by_id(id, self.args) if id else self.repo.get(self.args)