from .ControllerBase import ControllerBase
from Repositories import SocialRepository

class SocialController(ControllerBase):

    def __init__(self):
        self.repo = SocialRepository()
        super(SocialController, self).__init__()
        

    def get(self, id=None):
        self.parser.add_argument('name')
        self.parser.add_argument('origin')
        self.parser.add_argument('user_id')
        self.args = self.parser.parse_args()

        if id:
            return self.repo.get_by_id(id)
        else:
            return self.repo.get(self.args)