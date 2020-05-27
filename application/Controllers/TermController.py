from flask import request
from .ControllerBase import ControllerBase
from Repositories import TermRepository
from Utils import Helper

class TermController(ControllerBase):
    """This flask_restful API's Resource works like a controller to TermRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(TermController, self).__init__()
        self.args = Helper().add_request_data(self.parser, [
            's', 'parent_id', 'taxonomy_id', 'language_id', 'get_language', 'get_parent', 'get_children', 'get_taxonomy'])
        self.repo = TermRepository(session=self.session)

    def get(self, id=None, name=None):
        """Rewrite ControllerBase get method to apply customizations to the get http verb responder."""

        if str(request.url_rule) == '/api/term/suggestions/<name>':
            return self.repo.get_name_suggestions(name, self.args)
        elif id:
            return self.repo.get_by_id(id, self.args)
        else:
            return self.repo.get(self.args)