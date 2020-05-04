from .ControllerBase import ControllerBase
from Repositories import VariableRepository

class VariableController(ControllerBase):

    def get(self, id=None):
        repo = VariableRepository()
        self.parser.add_argument('s')
        self.args = self.parser.parse_args()
        if id:
            return repo.get_by_id(id)
        else:
            return repo.get(self.args)

    
    def post(self):
        repo = VariableRepository()
        return repo.create(self.request)


    def put(self, id=None):
        repo = VariableRepository()
        return repo.update(id, self.request)


    def delete(self, id=None):
        repo = VariableRepository()
        return repo.delete(id)