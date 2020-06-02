from .RepositoryBase import RepositoryBase
from Models import Field, FieldSchema, Post, Grouper, FieldContent, FieldFile, FieldText
from Validators import FieldValidator
from Utils import Paginate, FilterBuilder, Helper
from ErrorHandlers import BadRequestError

class FieldRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Field."""

    def __init__(self, session):
        super().__init__(session)
        
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        fb = FilterBuilder(Field, args)
        fb.set_equals_filters(['type', 'grouper_id', 'post_id'])

        try:
            fb.set_and_or_filter('s', 'or', [{'field':'name', 'type':'like'}, {'field':'description', 'type':'like'}])
        except Exception as e:
            raise BadRequestError(str(e))
        
        if not self.the_logged_user:
            self.joins.append(Post)
            fb.set_range_of_dates_filter(joined=Post, joined_key='publish_on')
            fb.filter += (Post.status == 'publish',)
        self.set_can_see_protected()
        if not self.can_see_protected:
            fb.filter += (Post.is_protected != True,)

        query = self.session.query(Field).join(*self.joins, isouter=True).filter(*fb.get_filter()).order_by(*fb.get_order_by())
        result = Paginate(query, fb.get_page(), fb.get_limit())
        schema = FieldSchema(many=True, exclude=self.get_exclude_fields(args, ['post', 'grouper']))
        return self.handle_success(result, schema, 'get', 'Field')
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        self.set_can_see_protected()
        fb = FilterBuilder(Post, {})
        self.joins.append(Post)
        if not self.the_logged_user:
            fb.set_range_of_dates_filter(joined=Post, joined_key='publish_on')
            fb.filter += (Post.status == 'publish',)
        self.set_can_see_protected()
        if not self.can_see_protected:
            fb.filter += (Post.is_protected != True,)
        
        fb.filter += (Field.id == id,)
        result = self.session.query(Field).join(*self.joins, isouter=True).filter(*fb.get_filter()).first()
        schema = FieldSchema(many=False, exclude=self.get_exclude_fields(args, ['post', 'grouper']))
        return self.handle_success(result, schema, 'get_by_id', 'Field')

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def process(session, data):
            field = Field()
            Helper().fill_object_from_data(field, data, ['name', 'description', 'type', 'order', 'grouper_id', 'post_id'])
            self.raise_if_has_different_parent_reference(data, session, [('grouper_id', 'post_id', Grouper)])
            self.add_foreign_keys(field, data, session, [('post_id', Post), ('grouper_id', Grouper)])
            session.add(field)
            session.commit()
            return self.handle_success(None, None, 'create', 'Field', field.id)

        return self.validate_before(process, request.get_json(), FieldValidator, self.session)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def process(session, data):
            
            def fn(session, field):

                if 'type' in data and data['type'] != field.type:
                    self.delete_children(session, id, [('field_id', FieldContent), ('field_id', FieldFile), ('field_id', FieldText)])

                Helper().fill_object_from_data(field, data, ['name', 'description', 'type', 'order', 'grouper_id', 'post_id'])
                self.raise_if_has_different_parent_reference(data, session, [('grouper_id', 'post_id', Grouper)])
                self.add_foreign_keys(field, data, session, [('post_id', Post), ('grouper_id', Grouper)])
                session.commit()
                return self.handle_success(None, None, 'update', 'Field', field.id)

            return self.run_if_exists(fn, Field, id, session)

        return self.validate_before(process, request.get_json(), FieldValidator, self.session, id=id)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def fn(session, field):
            self.delete_children(session, id, [('field_id', FieldContent), ('field_id', FieldFile), ('field_id', FieldText)])
            session.delete(field)
            session.commit()
            return self.handle_success(None, None, 'delete', 'Field', id)

        return self.run_if_exists(fn, Field, id, self.session)