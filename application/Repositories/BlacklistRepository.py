from .RepositoryBase import RepositoryBase
from Models import Blacklist, BlacklistSchema
from Validators import BlacklistValidator
from Utils import Paginate, FilterBuilder, Helper

class BlacklistRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Blacklist."""

    def __init__(self, session):
        super().__init__(session)
        
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        fb = FilterBuilder(Blacklist, args)
        fb.set_equals_filters(['type', 'target'])
        fb.set_like_filters(['value'])
        query = self.session.query(Blacklist).filter(*fb.get_filter()).order_by(*fb.get_order_by())
        result = Paginate(query, fb.get_page(), fb.get_limit())
        schema = BlacklistSchema(many=True)
        return self.handle_success(result, schema, 'get', 'Blacklist')
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        result = self.session.query(Blacklist).filter_by(id=id).first()
        schema = BlacklistSchema(many=False)
        return self.handle_success(result, schema, 'get_by_id', 'Blacklist')

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def process(session, data):
            blacklist = Blacklist()
            Helper().fill_object_from_data(blacklist, data, ['type', 'value', 'target'])
            session.add(blacklist)
            session.commit()
            return self.handle_success(None, None, 'create', 'Blacklist', blacklist.id)

        return self.validate_before(process, request.get_json(), BlacklistValidator, self.session)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def process(session, data):
            
            def fn(session, blacklist):
                Helper().fill_object_from_data(blacklist, data, ['type', 'value', 'target'])
                session.commit()
                return self.handle_success(None, None, 'update', 'Blacklist', blacklist.id)

            return self.run_if_exists(fn, Blacklist, id, self.session)

        return self.validate_before(process, request.get_json(), BlacklistValidator, self.session, id=id)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def fn(session, blacklist):
            session.delete(blacklist)
            session.commit()
            return self.handle_success(None, None, 'delete', 'Blacklist', id)

        return self.run_if_exists(fn, Blacklist, id, self.session)