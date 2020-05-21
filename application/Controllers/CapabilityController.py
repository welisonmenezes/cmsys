from .ControllerBase import ControllerBase
from Repositories import CapabilityRepository

class CapabilityController(ControllerBase):
    """This flask_restful API's Resource works like a controller to CapabilityRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(CapabilityController, self).__init__()
        self.parser.add_argument('description')
        self.parser.add_argument('type')
        self.parser.add_argument('target_id')
        self.parser.add_argument('can_write')
        self.parser.add_argument('can_read')
        self.parser.add_argument('can_delete')
        self.parser.add_argument('get_roles')
        self.args = self.parser.parse_args()
        self.repo = CapabilityRepository()