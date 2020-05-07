from .ControllerBase import ControllerBase
from Repositories import MediaRepository

class MediaController(ControllerBase):

    def __init__(self):
        self.repo = MediaRepository()
        super(MediaController, self).__init__()
        

    def get(self, id=None):
        self.parser.add_argument('download_file')
        self.parser.add_argument('return_file_data')
        self.parser.add_argument('s')
        self.parser.add_argument('type')
        self.parser.add_argument('origin')
        self.parser.add_argument('user_id')
        self.args = self.parser.parse_args()

        
        if (id and self.args['download_file'] == '1'):
            return self.repo.get_file(id)
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