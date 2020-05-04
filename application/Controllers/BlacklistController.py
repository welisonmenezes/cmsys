from .ControllerBase import ControllerBase
from Repositories import BlacklistRepository

class BlacklistController(ControllerBase):

    def get(self, id=None):
        repo = BlacklistRepository()
        self.parser.add_argument('value')
        self.parser.add_argument('type')
        self.parser.add_argument('target')
        self.args = self.parser.parse_args()

        if id:
            return repo.get_by_id(id)
        else:
            return repo.get(self.args)

    
    def post(self):
        repo = BlacklistRepository()
        return repo.create(self.request)


    def put(self, id=None):
        repo = BlacklistRepository()
        return repo.update(id, self.request)


    def delete(self, id=None):
        repo = BlacklistRepository()
        return repo.delete(id)