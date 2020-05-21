from .ControllerBase import ControllerBase
from Repositories import FieldRepository
from Utils import Helper

class FieldController(ControllerBase):
    """This flask_restful API's Resource works like a controller to FieldRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(FieldController, self).__init__()
        self.args = Helper().add_request_data(self.parser, ['s', 'type', 'grouper_id', 'post_id', 'get_post', 'get_grouper'])
        self.repo = FieldRepository()