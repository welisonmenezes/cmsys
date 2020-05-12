from .ControllerBase import ControllerBase
from Repositories import VariableRepository

class VariableController(ControllerBase):
    """This flask_restful API's Resource works like a controller to VariableRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(VariableController, self).__init__()
        self.repo = VariableRepository()


    def get(self, id=None):
        """Rewrite ControllerBase get method to apply customizations to the get http verb responder."""

        self.parser.add_argument('s')
        self.args = self.parser.parse_args()
        
        return self.repo.get_by_id(id) if id else self.repo.get(self.args)