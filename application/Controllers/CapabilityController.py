from .ControllerBase import ControllerBase
from Repositories import CapabilityRepository

class CapabilityController(ControllerBase):
    
    def get(self, id=None):
        repo = CapabilityRepository()
        self.parser.add_argument('get_roles')
        self.parser.add_argument('description')
        self.parser.add_argument('type')
        self.parser.add_argument('target_id')
        self.parser.add_argument('can_write')
        self.parser.add_argument('can_read')
        self.parser.add_argument('can_delete')
        self.args = self.parser.parse_args()

        if id:
            return repo.get_by_id(id)
        else:
            return repo.get(self.args)

    
    def post(self):
        repo = CapabilityRepository()
        return repo.create(self.request)


    def put(self, id=None):
        repo = CapabilityRepository()
        return repo.update(id, self.request)


    def delete(self, id=None):
        repo = CapabilityRepository()
        return repo.delete(id)