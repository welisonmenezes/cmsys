from .ControllerBase import ControllerBase
from Repositories import UserRepository
from Utils import Helper

class UserController(ControllerBase):
    """This flask_restful API's Resource works like a controller to UserRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(UserController, self).__init__()
        self.args = Helper().add_request_data(self.parser, [
            's', 'email', 'registered', 'status', 'role_id', 'get_role', 'get_socials',
            'get_medias', 'get_page', 'get_avatar', 'admin_new_owner'])
        self.repo = UserRepository(session=self.session)