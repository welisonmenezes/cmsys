from .ControllerBase import ControllerBase
from Repositories import CapabilityRepository

class CapabilityController(ControllerBase):
    """This flask_restful API's Resource works like a controller to CapabilityRepository"""

    def __init__(self):
        """Start the repository from which data will be written or retrieved"""

        super(CapabilityController, self).__init__()
        self.repo = CapabilityRepository()

    
    def get(self, id=None):
        """Rewrite ControllerBase get method to apply customizations to the get http verb responder"""

        self.parser.add_argument('get_roles')
        self.parser.add_argument('description')
        self.parser.add_argument('type')
        self.parser.add_argument('target_id')
        self.parser.add_argument('can_write')
        self.parser.add_argument('can_read')
        self.parser.add_argument('can_delete')
        self.args = self.parser.parse_args()

        return self.repo.get_by_id(id, self.args) if id else self.repo.get(self.args)