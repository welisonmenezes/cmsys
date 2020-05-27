from .RepositoryBase import RepositoryBase
from Models import Sector, SectorSchema, Menu
from Validators import SectorValidator
from Utils import Paginate, FilterBuilder, Helper
from ErrorHandlers import BadRequestError

class SectorRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Sector."""

    def __init__(self, session):
        super().__init__(session)
        
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        fb = FilterBuilder(Sector, args)
        
        try:
            fb.set_and_or_filter('s', 'or', [{'field':'name', 'type':'like'}, {'field':'description', 'type':'like'}])
        except Exception as e:
            raise BadRequestError(str(e))

        query = self.session.query(Sector).filter(*fb.get_filter()).order_by(*fb.get_order_by())
        result = Paginate(query, fb.get_page(), fb.get_limit())
        schema = SectorSchema(many=True, exclude=self.get_exclude_fields(args, ['menus']))
        return self.handle_success(result, schema, 'get', 'Sector')
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        result = self.session.query(Sector).filter_by(id=id).first()
        schema = SectorSchema(many=False, exclude=self.get_exclude_fields(args, ['menus']))
        return self.handle_success(result, schema, 'get_by_id', 'Sector')

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def process(session, data):
            sector = Sector()
            Helper().fill_object_from_data(sector, data, ['name', 'description'])
            session.add(sector)
            session.commit()
            return self.handle_success(None, None, 'create', 'Sector', sector.id)

        return self.validate_before(process, request.get_json(), SectorValidator, self.session)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def process(session, data):
            
            def fn(session, sector):
                Helper().fill_object_from_data(sector, data, ['name', 'description'])
                session.commit()
                return self.handle_success(None, None, 'update', 'Sector', sector.id)

            return self.run_if_exists(fn, Sector, id, session)

        return self.validate_before(process, request.get_json(), SectorValidator, self.session, id=id)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def fn(session, sector):
            
            if sector.menus:
                raise BadRequestError('You cannot delete this Sector because it has a related Menu.')

            session.delete(sector)
            session.commit()
            return self.handle_success(None, None, 'delete', 'Sector', id)

        return self.run_if_exists(fn, Sector, id, self.session)