from .RepositoryBase import RepositoryBase
from Models import Sector, SectorSchema
from Validators import SectorValidator
from Utils import Paginate, ErrorHandler, FilterBuilder

class SectorRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Sector."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(Sector, args)
            
            try:
                fb.set_and_or_filter('s', 'or', [{'field':'name', 'type':'like'}, {'field':'description', 'type':'like'}])
            except Exception as e:
                return ErrorHandler().get_error(400, str(e))

            query = session.query(Sector).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = SectorSchema(many=True)
            return self.handle_success(result, schema, 'get', 'Sector')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(Sector).filter_by(id=id).first()
            schema = SectorSchema(many=False)
            return self.handle_success(result, schema, 'get_by_id', 'Sector')

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):

                sector = Sector(
                    name = data['name'],
                    description = data['description']
                )
                session.add(sector)
                session.commit()
                return self.handle_success(None, None, 'create', 'Sector', sector.id)

            return self.validate_before(process, request.get_json(), SectorValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):
                
                def fn(session, sector):
                    sector.name = data['name']
                    sector.description = data['description']
                    session.commit()
                    return self.handle_success(None, None, 'update', 'Sector', sector.id)

                return self.run_if_exists(fn, Sector, id, session)

            return self.validate_before(process, request.get_json(), SectorValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):

            def fn(session, sector):

                # TODO: forbid delete if it has a menu related.

                session.delete(sector)
                session.commit()
                return self.handle_success(None, None, 'delete', 'Sector', id)

            return self.run_if_exists(fn, Sector, id, session)

        return self.response(run, True)