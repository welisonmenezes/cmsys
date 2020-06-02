from .RepositoryBase import RepositoryBase
from Models import FieldText, FieldTextSchema, Field, Grouper, Post
from Validators import FieldTextValidator
from Utils import Paginate, FilterBuilder, Helper
from ErrorHandlers import BadRequestError

class FieldTextRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of FieldText."""

    def __init__(self, session):
        super().__init__(session)
        
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        fb = FilterBuilder(FieldText, args)
        fb.set_like_filters(['content'])
        fb.set_equals_filters(['field_id', 'grouper_id', 'post_id'])
        self.set_protection_to_child_post(fb)
        query = self.session.query(FieldText).join(*self.joins, isouter=True).filter(*fb.get_filter()).order_by(*fb.get_order_by())
        result = Paginate(query, fb.get_page(), fb.get_limit())
        schema = FieldTextSchema(many=True)
        return self.handle_success(result, schema, 'get', 'FieldText')
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        fb = FilterBuilder(Post, {})
        self.set_protection_to_child_post(fb)
        fb.filter += (FieldText.id == id,)
        result = self.session.query(FieldText).join(*self.joins, isouter=True).filter(*fb.get_filter()).first()
        schema = FieldTextSchema(many=False)
        return self.handle_success(result, schema, 'get_by_id', 'FieldText')

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def process(session, data):
            field_text = FieldText()
            Helper().fill_object_from_data(field_text, data, ['content'])
            self.raise_if_has_different_parent_reference(data, session, [('field_id', 'grouper_id', Field), ('field_id', 'post_id', Field)])
            self.add_foreign_keys_field_type('short-text', field_text, data, session, [('field_id', Field), ('grouper_id', Grouper), ('post_id', Post)])
            session.add(field_text)
            session.commit()
            return self.handle_success(None, None, 'create', 'FieldText', field_text.id)

        return self.validate_before(process, request.get_json(), FieldTextValidator, self.session)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def process(session, data):
            
            def fn(session, field_text):
                Helper().fill_object_from_data(field_text, data, ['content'])
                self.raise_if_has_different_parent_reference(data, session, [('field_id', 'grouper_id', Field), ('field_id', 'post_id', Field)])
                self.add_foreign_keys_field_type('short-text', field_text, data, session, [('field_id', Field), ('grouper_id', Grouper), ('post_id', Post)], id)
                session.commit()
                return self.handle_success(None, None, 'update', 'FieldText', field_text.id)

            return self.run_if_exists(fn, FieldText, id, session)

        return self.validate_before(process, request.get_json(), FieldTextValidator, self.session, id=id)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def fn(session, field_text):
            session.delete(field_text)
            session.commit()
            return self.handle_success(None, None, 'delete', 'FieldText', id)

        return self.run_if_exists(fn, FieldText, id, self.session)