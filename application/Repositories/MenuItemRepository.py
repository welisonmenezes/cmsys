from .RepositoryBase import RepositoryBase
from Models import MenuItem, MenuItemSchema, Menu
from Validators import MenuItemValidator
from Utils import Paginate, ErrorHandler, FilterBuilder

class MenuItemRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of MenuItem."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(MenuItem, args)
            fb.set_equals_filter('type')
            fb.set_equals_filter('behavior')
            fb.set_equals_filter('url')
            fb.set_equals_filter('menu_id')
            fb.set_equals_filter('parent_id')
            fb.set_like_filter('title')

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

                menu_item = MenuItem(
                    type = data['type'],
                    behavior = data['behavior'],
                    url = data['url'],
                    title = data['title'],
                    order = data['order']
                )

                can_add_ref = self.forbid_save_with_different_parent_reference(data, session, MenuItem, [('parent_id', 'menu_id')])
                if can_add_ref != True:
                    return can_add_ref

                if 'target_id' in data and data['target_id'] != '':
                    menu_item.target_id = data['target_id']

                fk_was_added = self.add_foreign_keys(menu_item, data, session, [('parent_id', MenuItem), ('menu_id', Menu)])
                if fk_was_added != True:
                    return fk_was_added

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
                    menu_item.type = data['type']
                    menu_item.behavior = data['behavior']
                    menu_item.url = data['url']
                    menu_item.title = data['title']
                    menu_item.order = data['order']

                    can_add_ref = self.forbid_save_with_different_parent_reference(data, session, MenuItem, [('parent_id', 'menu_id')])
                    if can_add_ref != True:
                        return can_add_ref

                    if 'target_id' in data and data['target_id'] != '':
                        menu_item.target_id = data['target_id']

                    fk_was_added = self.add_foreign_keys(menu_item, data, session, [('parent_id', MenuItem), ('menu_id', Menu)])
                    if fk_was_added != True:
                        return fk_was_added

                    if menu_item.parent_id and int(menu_item.parent_id) == int(id):
                        return ErrorHandler().get_error(400, 'The MenuItem cannot be parent of yourself.')

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