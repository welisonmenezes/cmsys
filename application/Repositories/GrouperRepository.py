from .RepositoryBase import RepositoryBase
from Models import Grouper, GrouperSchema
from Validators import GrouperValidator
from Utils import Paginate, ErrorHandler, FilterBuilder

class GrouperRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Grouper."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(Grouper, args)
            # fb.set_equals_filter('type')
            # fb.set_equals_filter('target')
            # fb.set_like_filter('value')

            query = session.query(Grouper).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = GrouperSchema(many=True)
            return self.handle_success(result, schema, 'get', 'Grouper')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(Grouper).filter_by(id=id).first()
            schema = GrouperSchema(many=False)
            return self.handle_success(result, schema, 'get_by_id', 'Grouper')

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):

                grouper = Grouper(
                    name = data['name'],
                    description = data['description'],
                    order = data['order'],
                    #parent_id = data['parent_id'],
                    post_id = data['post_id']
                )
                session.add(grouper)
                session.commit()
                return self.handle_success(None, None, 'create', 'Grouper', grouper.id)

            return self.validate_before(process, request.get_json(), GrouperValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):
                
                def fn(session, grouper):
                    grouper.name = data['name']
                    grouper.description = data['description']
                    grouper.order = data['order']
                    #grouper.parent_id = data['parent_id']
                    grouper.post_id = data['post_id']
                    session.commit()
                    return self.handle_success(None, None, 'update', 'Grouper', grouper.id)

                return self.run_if_exists(fn, Grouper, id, session)

            return self.validate_before(process, request.get_json(), GrouperValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):

            def fn(session, grouper):
                session.delete(grouper)
                session.commit()
                return self.handle_success(None, None, 'delete', 'Grouper', id)

            return self.run_if_exists(fn, Grouper, id, session)

        return self.response(run, True)