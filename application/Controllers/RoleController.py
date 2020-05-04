from .ControllerBase import ControllerBase
from Repositories import RoleRepository

class RoleController(ControllerBase):

    def __init__(self):
        self.repo = RoleRepository()
        super(RoleController, self).__init__()

    
    def get(self, id=None):
        self.parser.add_argument('get_capabilities')
        self.parser.add_argument('name')
        self.parser.add_argument('description')
        self.parser.add_argument('can_access_admin')
        self.parser.add_argument('capability_description')
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