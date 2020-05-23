from .ControllerBase import ControllerBase
from Repositories import TermRepository
from Utils import Helper

class TermController(ControllerBase):
    """This flask_restful API's Resource works like a controller to TermRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(TermController, self).__init__()
        self.args = Helper().add_request_data(self.parser, [
            's', 'parent_id', 'taxonomy_id', 'language_id', 'get_posts', 'get_language', 'get_parent', 'get_children'])
        print(self.args)
        self.repo = TermRepository()