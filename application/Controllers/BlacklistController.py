from .ControllerBase import ControllerBase
from Repositories import BlacklistRepository

class BlacklistController(ControllerBase):

    def __init__(self):
        self.repo = BlacklistRepository()
        super(BlacklistController, self).__init__()
        

    def get(self, id=None):
        self.parser.add_argument('value')
        self.parser.add_argument('type')
        self.parser.add_argument('target')
        self.args = self.parser.parse_args()

        if id:
            return self.repo.get_by_id(id)
        else:
            return self.repo.get(self.args)

    
    def post(self):
        return self.repo.create(self.request)


    def put(self, id=None):
        return self.repo.update(id, self.request)


    def delete(self, id=None):
        return self.repo.delete(id)