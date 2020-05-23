from flask import request
from .ControllerBase import ControllerBase
from Repositories import PostRepository
from Utils import Helper

class PostController(ControllerBase):
    """This flask_restful API's Resource works like a controller to PostRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(PostController, self).__init__()
        self.repo = PostRepository()
        

    def get(self, id=None, name=None):
        """Rewrite ControllerBase get method to apply customizations to the get http verb responder."""

        self.args = Helper().add_request_data(self.parser, [
            's', 'status', 'created', 'parent_id', 'post_type_id', 'user_id', 'language_id', 'get_user', 'get_language', 
            'get_parent', 'get_children', 'get_post_type', 'get_nests', 'get_groupers', 'remove_foreign_keys', 'get_terms', 'term_id'])
        
        if str(request.url_rule) == '/api/post/suggestions/<name>':
            return self.repo.get_name_suggestions(name, self.args)
        elif id:
            return self.repo.get_by_id(id, self.args)
        else:
            return self.repo.get(self.args)