from .ControllerBase import ControllerBase
from Repositories import VariableRepository

class VariableController(ControllerBase):

    def __init__(self):
        self.repo = VariableRepository()
        super(VariableController, self).__init__()


    def get(self, id=None):
        self.parser.add_argument('s')
        self.args = self.parser.parse_args()
        
        return self.repo.get_by_id(id) if id else self.repo.get(self.args)