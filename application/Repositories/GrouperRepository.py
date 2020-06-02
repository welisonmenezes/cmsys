from .RepositoryBase import RepositoryBase
from Models import Grouper, GrouperSchema, Post, Field, FieldFile, FieldContent, FieldText
from Validators import GrouperValidator
from Utils import Paginate, FilterBuilder, Helper
from ErrorHandlers import BadRequestError

class GrouperRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Grouper."""

    def __init__(self, session):
        super().__init__(session)
        
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        fb = FilterBuilder(Grouper, args)
        fb.set_equals_filters(['parent_id', 'post_id'])
        
        try:
            fb.set_and_or_filter('s', 'or', [{'field':'name', 'type':'like'}, {'field':'description', 'type':'like'}])
        except Exception as e:
            raise BadRequestError(str(e))
        
        self.set_protection_to_child_post(fb)
        query = self.session.query(Grouper).join(*self.joins, isouter=True).filter(*fb.get_filter()).order_by(*fb.get_order_by())
        result = Paginate(query, fb.get_page(), fb.get_limit())
        schema = GrouperSchema(many=True, exclude=self.get_exclude_fields(args, ['parent', 'post', 'children', 'fields']))
        return self.handle_success(result, schema, 'get', 'Grouper')
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        fb = FilterBuilder(Post, {})
        self.set_protection_to_child_post(fb)
        fb.filter += (Grouper.id == id,)
        result = self.session.query(Grouper).join(*self.joins, isouter=True).filter(*fb.get_filter()).first()
        schema = GrouperSchema(many=False, exclude=self.get_exclude_fields(args, ['parent', 'post', 'children', 'fields']))
        return self.handle_success(result, schema, 'get_by_id', 'Grouper')

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def process(session, data):
            grouper = Grouper()
            Helper().fill_object_from_data(grouper, data, ['name', 'description', 'order'])
            self.raise_if_has_different_parent_reference(data, session, [('parent_id', 'post_id', Grouper)])
            self.add_foreign_keys(grouper, data, session, [('parent_id', Grouper), ('post_id', Post)])
            session.add(grouper)
            session.commit()
            return self.handle_success(None, None, 'create', 'Grouper', grouper.id)

        return self.validate_before(process, request.get_json(), GrouperValidator, self.session)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def process(session, data):
            
            def fn(session, grouper):
                Helper().fill_object_from_data(grouper, data, ['name', 'description', 'order'])
                self.raise_if_has_different_parent_reference(data, session, [('parent_id', 'post_id', Grouper)])
                self.add_foreign_keys(grouper, data, session, [('parent_id', Grouper), ('post_id', Post)])

                if grouper.parent_id and int(grouper.parent_id) == int(id):
                    raise BadRequestError('The Grouper cannot be parent of yourself.')

                session.commit()
                return self.handle_success(None, None, 'update', 'Grouper', grouper.id)

            return self.run_if_exists(fn, Grouper, id, session)

        return self.validate_before(process, request.get_json(), GrouperValidator, self.session, id=id)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def fn(session, grouper):
            self.delete_children(session, id, [('grouper_id', FieldContent), ('grouper_id', FieldFile), ('grouper_id', FieldText), ('grouper_id', Field)])
            self.delete_deep_chidren(grouper, Grouper, session)
            session.delete(grouper)
            session.commit()
            return self.handle_success(None, None, 'delete', 'Grouper', id)

        return self.run_if_exists(fn, Grouper, id, self.session)