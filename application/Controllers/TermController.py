from .ControllerBase import ControllerBase
from Repositories import TermRepository
from Utils import Helper

class TermController(ControllerBase):
    """This flask_restful API's Resource works like a controller to TermRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(TermController, self).__init__()
        self.args = Helper().add_request_data(self.parser, [])
        print(self.args)
        self.repo = TermRepository()