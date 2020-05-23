from .RepositoryBase import RepositoryBase
from Models import Term, TermSchema
from Validators import TermValidator
from Utils import Paginate, FilterBuilder, Helper

class TermRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Term."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(Term, args)
            #fb.set_equals_filters(['type', 'target'])
            #fb.set_like_filters(['value'])
            query = session.query(Term).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = TermSchema(many=True)
            return self.handle_success(result, schema, 'get', 'Term')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(Term).filter_by(id=id).first()
            schema = TermSchema(many=False)
            return self.handle_success(result, schema, 'get_by_id', 'Term')

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):
                term = Term()
                Helper().fill_object_from_data(term, data, ['name', 'display_name', 'description', 'parent_id', 'page_id', 'taxonomy_id', 'language_id'])
                session.add(term)
                session.commit()
                return self.handle_success(None, None, 'create', 'Term', term.id)

            return self.validate_before(process, request.get_json(), TermValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):
                
                def fn(session, term):
                    Helper().fill_object_from_data(term, data, ['name', 'display_name', 'description', 'parent_id', 'page_id', 'taxonomy_id', 'language_id'])
                    session.commit()
                    return self.handle_success(None, None, 'update', 'Term', term.id)

                return self.run_if_exists(fn, Term, id, session)

            return self.validate_before(process, request.get_json(), TermValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):

            def fn(session, term):
                session.delete(term)
                session.commit()
                return self.handle_success(None, None, 'delete', 'Term', id)

            return self.run_if_exists(fn, Term, id, session)

        return self.response(run, True)