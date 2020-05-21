from .ControllerBase import ControllerBase
from Repositories import GrouperRepository
from Utils import Helper

class GrouperController(ControllerBase):
    """This flask_restful API's Resource works like a controller to GrouperRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(GrouperController, self).__init__()
        self.args = Helper().add_request_data(self.parser, ['s', 'parent_id', 'post_id', 'get_parent', 'get_children', 'get_post', 'get_fields'])
        self.repo = GrouperRepository()