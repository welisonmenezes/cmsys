from .ControllerBase import ControllerBase
from Repositories import CapabilityRepository

class CapabilityController(ControllerBase):

    def __init__(self):
        self.repo = CapabilityRepository()
        super(CapabilityController, self).__init__()

    
    def get(self, id=None):
        self.parser.add_argument('get_children')
        self.parser.add_argument('description')
        self.parser.add_argument('type')
        self.parser.add_argument('target_id')
        self.parser.add_argument('can_write')
        self.parser.add_argument('can_read')
        self.parser.add_argument('can_delete')
        self.args = self.parser.parse_args()

        if id:
            return self.repo.get_by_id(id, self.args)
        else:
            return self.repo.get(self.args)