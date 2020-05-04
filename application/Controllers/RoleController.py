from .ControllerBase import ControllerBase
from Repositories import RoleRepository

class RoleController(ControllerBase):
    
    def get(self, id=None):
        repo = RoleRepository()
        self.parser.add_argument('get_capabilities')
        self.parser.add_argument('name')
        self.parser.add_argument('description')
        self.parser.add_argument('can_access_admin')
        self.parser.add_argument('capability_description')
        self.args = self.parser.parse_args()
        
        if id:
            return repo.get_by_id(id)
        else:
            return repo.get(self.args)

    
    def post(self):
        repo = RoleRepository()
        return repo.create(self.request)


    def put(self, id=None):
        repo = RoleRepository()
        return repo.update(id, self.request)


    def delete(self, id=None):
        repo = RoleRepository()
        return repo.delete(id)