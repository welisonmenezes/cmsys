from .RepositoryBase import RepositoryBase
from Models import Taxonomy, TaxonomySchema
from Validators import TaxonomyValidator
from Utils import Paginate, FilterBuilder, Helper
from ErrorHandlers import BadRequestError

class TaxonomyRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Taxonomy."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(Taxonomy, args)

            try:
                fb.set_and_or_filter('s', 'or', [{'field':'name', 'type':'like'}, {'field':'description', 'type':'like'}])
            except Exception as e:
                raise BadRequestError(str(e))

            query = session.query(Taxonomy).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = TaxonomySchema(many=True, exclude=self.get_exclude_fields(args, ['post_types', 'terms']))
            return self.handle_success(result, schema, 'get', 'Taxonomy')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(Taxonomy).filter_by(id=id).first()
            schema = TaxonomySchema(many=False, exclude=self.get_exclude_fields(args, ['post_types', 'terms']))
            return self.handle_success(result, schema, 'get_by_id', 'Taxonomy')

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):
                taxonomy = Taxonomy()
                Helper().fill_object_from_data(taxonomy, data, ['name', 'description', 'has_child'])
                session.add(taxonomy)
                session.commit()
                return self.handle_success(None, None, 'create', 'Taxonomy', taxonomy.id)

            return self.validate_before(process, request.get_json(), TaxonomyValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):
                
                def fn(session, taxonomy):
                    Helper().fill_object_from_data(taxonomy, data, ['name', 'description', 'has_child'])
                    session.commit()
                    return self.handle_success(None, None, 'update', 'Taxonomy', taxonomy.id)

                return self.run_if_exists(fn, Taxonomy, id, session)

            return self.validate_before(process, request.get_json(), TaxonomyValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):

            def fn(session, taxonomy):
                if taxonomy.terms:
                    raise BadRequestError('You cannot delete this Taxonomy because it has a related Term')

                if taxonomy.post_types:
                    raise BadRequestError('You cannot delete this Taxonomy because it has a related Post_Type')

                session.delete(taxonomy)
                session.commit()
                return self.handle_success(None, None, 'delete', 'Taxonomy', id)

            return self.run_if_exists(fn, Taxonomy, id, session)

        return self.response(run, True)