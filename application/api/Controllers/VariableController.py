from .ControllerBase import ControllerBase
from Repositories import VariableRepository
from Utils import Helper

class VariableController(ControllerBase):
    """This flask_restful API's Resource works like a controller to VariableRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(VariableController, self).__init__()
        self.args = Helper().add_request_data(self.parser, ['s'])
        self.repo = VariableRepository(session=self.session)