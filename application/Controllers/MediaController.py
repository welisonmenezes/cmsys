from flask import request
from .ControllerBase import ControllerBase
from Repositories import MediaRepository

class MediaController(ControllerBase):
    """This flask_restful API's Resource works like a controller to MediaRepository."""

    def __init__(self):
        """Starts the repository from which data will be written or retrieved."""

        super(MediaController, self).__init__()
        self.repo = MediaRepository()


    def get(self, id=None, name=None):
        """Rewrite ControllerBase get method to apply customizations to the get http verb responder."""

        self.parser.add_argument('download_file')
        self.parser.add_argument('return_file_data')
        self.parser.add_argument('s')
        self.parser.add_argument('type')
        self.parser.add_argument('origin')
        self.parser.add_argument('created')
        self.parser.add_argument('user_id')
        self.args = self.parser.parse_args()

        if str(request.url_rule) == '/api/media/preview/<id>':
            return self.repo.get_image_preview(id)
        elif str(request.url_rule) == '/api/media/suggestions/<name>':
            return self.repo.get_name_suggestions(name, self.args)
        elif (id and self.args['download_file'] == '1'):
            return self.repo.get_file(id, self.args)
        elif id:
            return self.repo.get_by_id(id, self.args)
        else:
            return self.repo.get(self.args)