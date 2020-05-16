from flask import request
from .ControllerBase import ControllerBase
from Repositories import PostRepository

class PostController(ControllerBase):
    """This flask_restful API's Resource works like a controller to PostRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(PostController, self).__init__()
        self.repo = PostRepository()
        

    def get(self, id=None, name=None):
        """Rewrite ControllerBase get method to apply customizations to the get http verb responder."""

        self.parser.add_argument('s')
        self.parser.add_argument('status')
        self.parser.add_argument('created')
        self.parser.add_argument('parent_id')
        self.parser.add_argument('post_type_id')
        self.parser.add_argument('user_id')
        self.parser.add_argument('language_id')
        self.parser.add_argument('get_user')
        self.parser.add_argument('get_language')
        self.parser.add_argument('remove_foreign_keys')
        self.args = self.parser.parse_args()
        
        if str(request.url_rule) == '/api/post/suggestions/<name>':
            return self.repo.get_name_suggestions(name, self.args)
        elif id:
            return self.repo.get_by_id(id, self.args)
        else:
            return self.repo.get(self.args)