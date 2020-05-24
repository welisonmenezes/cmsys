from .ControllerBase import ControllerBase
from Repositories import TaxonomyRepository
from Utils import Helper

class TaxonomyController(ControllerBase):
    """This flask_restful API's Resource works like a controller to TaxonomyRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(TaxonomyController, self).__init__()
        self.args = Helper().add_request_data(self.parser, [])
        self.repo = TaxonomyRepository()