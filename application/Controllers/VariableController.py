from .ControllerBase import ControllerBase
from Repositories import VariableRepository

class VariableController(ControllerBase):
    """This flask_restful API's Resource works like a controller to VariableRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(VariableController, self).__init__()
        self.parser.add_argument('s')
        self.args = self.parser.parse_args()
        self.repo = VariableRepository()