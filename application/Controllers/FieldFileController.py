from .ControllerBase import ControllerBase
from Repositories import FieldFileRepository
from Utils import Helper

class FieldFileController(ControllerBase):
    """This flask_restful API's Resource works like a controller to FieldFileRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(FieldFileController, self).__init__()
        self.args = Helper().add_request_data(self.parser, ['field_id', 'media_id', 'grouper_id', 'post_id'])
        self.repo = FieldFileRepository(session=self.session)