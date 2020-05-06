from .ControllerBase import ControllerBase
from Repositories import MediaRepository

class MediaController(ControllerBase):

    def __init__(self):
        self.repo = MediaRepository()
        super(MediaController, self).__init__()
        

    def get(self, id=None):
        # self.parser.add_argument('value')
        # self.parser.add_argument('type')
        self.parser.add_argument('get_preview')
        self.parser.add_argument('get_file')
        self.args = self.parser.parse_args()

        
        if (id and self.args['get_preview'] == '1'):
            return self.repo.get_preview(id, self.args)
        elif id:
            return self.repo.get_by_id(id, self.args)
        else:
            return self.repo.get(self.args)

    
    def post(self):
        return self.repo.create(self.request)


    def put(self, id=None):
        return self.repo.update(id, self.request)


    def delete(self, id=None):
        return self.repo.delete(id)