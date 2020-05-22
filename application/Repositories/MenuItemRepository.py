from .RepositoryBase import RepositoryBase
from Models import MenuItem, MenuItemSchema, Menu
from Validators import MenuItemValidator
from Utils import Paginate, FilterBuilder, Helper
from ErrorHandlers import BadRequestError

class MenuItemRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of MenuItem."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(MenuItem, args)
            fb.set_equals_filters(['type', 'behavior', 'url', 'menu_id', 'parent_id'])
            fb.set_like_filters(['title'])
            query = session.query(MenuItem).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = MenuItemSchema(many=True, exclude=self.get_exclude_fields(args, ['parent', 'children', 'menu']))
            return self.handle_success(result, schema, 'get', 'MenuItem')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(MenuItem).filter_by(id=id).first()
            schema = MenuItemSchema(many=False, exclude=self.get_exclude_fields(args, ['parent', 'children', 'menu']))
            return self.handle_success(result, schema, 'get_by_id', 'MenuItem')

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):
                menu_item = MenuItem()
                Helper().fill_object_from_data(menu_item, data, ['type', 'behavior', 'url', 'title', 'order'])
                self.raise_if_has_different_parent_reference(data, session, [('parent_id', 'menu_id', MenuItem)])

                if 'target_id' in data and data['target_id'] != '':
                    menu_item.target_id = data['target_id']

                self.add_foreign_keys(menu_item, data, session, [('parent_id', MenuItem), ('menu_id', Menu)])

                session.add(menu_item)
                session.commit()
                return self.handle_success(None, None, 'create', 'MenuItem', menu_item.id)

            return self.validate_before(process, request.get_json(), MenuItemValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):
                
                def fn(session, menu_item):
                    Helper().fill_object_from_data(menu_item, data, ['type', 'behavior', 'url', 'title', 'order'])
                    self.raise_if_has_different_parent_reference(data, session, [('parent_id', 'menu_id', MenuItem)])

                    if 'target_id' in data and data['target_id'] != '':
                        menu_item.target_id = data['target_id']

                    self.add_foreign_keys(menu_item, data, session, [('parent_id', MenuItem), ('menu_id', Menu)])

                    if menu_item.parent_id and int(menu_item.parent_id) == int(id):
                        raise BadRequestError('The MenuItem cannot be parent of yourself.')

                    session.commit()
                    return self.handle_success(None, None, 'update', 'MenuItem', menu_item.id)

                return self.run_if_exists(fn, MenuItem, id, session)

            return self.validate_before(process, request.get_json(), MenuItemValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):

            def fn(session, menu_item):
                self.delete_deep_chidren(menu_item, MenuItem, session)
                session.delete(menu_item)
                session.commit()
                return self.handle_success(None, None, 'delete', 'MenuItem', id)

            return self.run_if_exists(fn, MenuItem, id, session)

        return self.response(run, True)