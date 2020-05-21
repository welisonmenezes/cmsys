from .ControllerBase import ControllerBase
from Repositories import CapabilityRepository
from Utils import Helper

class CapabilityController(ControllerBase):
    """This flask_restful API's Resource works like a controller to CapabilityRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(CapabilityController, self).__init__()
        self.args = Helper().add_request_data(self.parser, ['description', 'type', 'target_id', 'can_write', 'can_read', 'can_delete', 'get_roles'])
        self.repo = CapabilityRepository()