from .ControllerBase import ControllerBase
from Repositories import FieldTextRepository
from Utils import Helper

class FieldTextController(ControllerBase):
    """This flask_restful API's Resource works like a controller to FieldTextRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(FieldTextController, self).__init__()
        self.args = Helper().add_request_data(self.parser, ['content', 'field_id', 'grouper_id', 'post_id'])
        self.repo = FieldTextRepository()