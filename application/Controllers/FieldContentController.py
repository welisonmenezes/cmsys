from .ControllerBase import ControllerBase
from Repositories import FieldContentRepository
from Utils import Helper

class FieldContentController(ControllerBase):
    """This flask_restful API's Resource works like a controller to FieldContentRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(FieldContentController, self).__init__()
        self.args = Helper().add_request_data(self.parser, ['content', 'field_id', 'grouper_id', 'post_id'])
        self.repo = FieldContentRepository(session=self.session)