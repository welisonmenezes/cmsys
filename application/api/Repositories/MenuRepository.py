from .RepositoryBase import RepositoryBase
from Models import Menu, MenuSchema, Language, Sector, MenuItem
from Validators import MenuValidator
from Utils import Paginate, FilterBuilder, Helper
from ErrorHandlers import BadRequestError

# TODO: from menu to be able to save/update/delete menu items

class MenuRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Menu."""

    def __init__(self, session):
        super().__init__(session)
        
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        fb = FilterBuilder(Menu, args)
        fb.set_equals_filters(['language_id'])

        try:
            fb.set_and_or_filter('s', 'or', [{'field':'name', 'type':'like'}, {'field':'description', 'type':'like'}])
        except Exception as e:
            raise BadRequestError(str(e))

        query = self.session.query(Menu).filter(*fb.get_filter()).order_by(*fb.get_order_by())
        result = Paginate(query, fb.get_page(), fb.get_limit())
        schema = MenuSchema(many=True, exclude=self.get_exclude_fields(args, ['language', 'sectors', 'items']))
        return self.handle_success(result, schema, 'get', 'Menu')
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        result = self.session.query(Menu).filter_by(id=id).first()
        schema = MenuSchema(many=False, exclude=self.get_exclude_fields(args, ['language', 'sectors', 'items']))
        return self.handle_success(result, schema, 'get_by_id', 'Menu')

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def process(session, data):
            menu = Menu()
            Helper().fill_object_from_data(menu, data, ['name', 'order', 'description'])
            self.add_foreign_keys(menu, data, session, [('language_id', Language)])
            self.add_many_to_many_relationship('sectors', menu, data, Sector, session)
            session.add(menu)
            session.commit()
            return self.handle_success(None, None, 'create', 'Menu', menu.id)

        return self.validate_before(process, request.get_json(), MenuValidator, self.session)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def process(session, data):
            
            def fn(session, menu):
                Helper().fill_object_from_data(menu, data, ['name', 'order', 'description'])
                self.add_foreign_keys(menu, data, session, [('language_id', Language)])
                self.edit_many_to_many_relationship('sectors', menu, data, Sector, session)
                session.commit()
                return self.handle_success(None, None, 'update', 'Menu', menu.id)

            return self.run_if_exists(fn, Menu, id, session)

        return self.validate_before(process, request.get_json(), MenuValidator, self.session, id=id)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def fn(session, menu):
            self.delete_children(session, id, [('menu_id', MenuItem)])
            session.delete(menu)
            session.commit()
            return self.handle_success(None, None, 'delete', 'Menu', id)

        return self.run_if_exists(fn, Menu, id, self.session)