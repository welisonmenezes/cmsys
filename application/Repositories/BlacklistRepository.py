from sqlalchemy import or_
from Models import Blacklist, BlacklistSchema
from Validators import BlacklistValidator
from Utils import Paginate, ErrorHandler
from .RepositoryBase import RepositoryBase

class BlacklistRepository(RepositoryBase):
    
    def get(self, args):
        def fn(session):
            return {'method': 'get'}

        return self.response(fn, False)
        

    def get_by_id(self, id):
        def fn(session):
            return {'method': 'get by id'}

        return self.response(fn, False)

    
    def create(self, request):
        def fn(session):
            return {'method': 'create'}

        return self.response(fn, True)


    def update(self, id, request):
        def fn(session):
            return {'method': 'update'}

        return self.response(fn, True)


    def delete(self, id):
        def fn(session):
            return {'method': 'delete'}

        return self.response(fn, True)