from .ControllerBase import ControllerBase
from Repositories import RoleRepository
from Utils import Helper

class RoleController(ControllerBase):
    """This flask_restful API's Resource works like a controller to RoleRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(RoleController, self).__init__()
        self.args = Helper().add_request_data(self.parser, ['get_capabilities', 'name', 'description', 'can_access_admin', 'capability_description'])
        self.repo = RoleRepository()