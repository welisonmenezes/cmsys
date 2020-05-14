from .RepositoryBase import RepositoryBase
from Models import Blacklist, BlacklistSchema
from Validators import BlacklistValidator
from Utils import Paginate, ErrorHandler, FilterBuilder

class BlacklistRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Blacklist."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(Blacklist, args)
            fb.set_equals_filter('type')
            fb.set_equals_filter('target')
            fb.set_like_filter('value')

            query = session.query(Blacklist).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = BlacklistSchema(many=True)
            return self.handle_success(result, schema, 'get', 'Blacklist')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(Blacklist).filter_by(id=id).first()
            schema = BlacklistSchema(many=False)
            return self.handle_success(result, schema, 'get_by_id', 'Blacklist')

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):

                blacklist = Blacklist(
                    type = data['type'],
                    value = data['value'],
                    target = data['target']
                )
                session.add(blacklist)
                session.commit()
                return self.handle_success(None, None, 'create', 'Blacklist', blacklist.id)

            return self.validate_before(process, request.get_json(), BlacklistValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):
                blacklist = session.query(Blacklist).filter_by(id=id).first()

                if (blacklist):
                    blacklist.type = data['type']
                    blacklist.value = data['value']
                    blacklist.target = data['target']
                    session.commit()
                    return self.handle_success(None, None, 'update', 'Blacklist', blacklist.id)

                else:
                    return ErrorHandler().get_error(404, 'No Blacklist found.')

            return self.validate_before(process, request.get_json(), BlacklistValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):
            blacklist = session.query(Blacklist).filter_by(id=id).first()

            if (blacklist):
                session.delete(blacklist)
                session.commit()
                return self.handle_success(None, None, 'delete', 'Blacklist', id)

            else:
                return ErrorHandler().get_error(404, 'No Blacklist found.')

        return self.response(run, True)