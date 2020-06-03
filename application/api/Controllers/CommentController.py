from .ControllerBase import ControllerBase
from Repositories import CommentRepository
from Utils import Helper

class CommentController(ControllerBase):
    """This flask_restful API's Resource works like a controller to CommentRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(CommentController, self).__init__()
        self.args = Helper().add_request_data(self.parser, [
            'comment', 'status', 'origin_ip', 'origin_agent', 'created', 'parent_id', 'user_id', 'post_id',
            'language_id', 'get_user', 'get_language',  'get_post', 'get_parent', 'get_children'])
        self.repo = CommentRepository(session=self.session)