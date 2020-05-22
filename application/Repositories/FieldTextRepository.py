from .RepositoryBase import RepositoryBase
from Models import FieldText, FieldTextSchema, Field, Grouper, Post
from Validators import FieldTextValidator
from Utils import Paginate, FilterBuilder, Helper

# TODO: forbid save/update if field type is equals short-text

class FieldTextRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of FieldText."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(FieldText, args)
            fb.set_like_filters(['content'])
            fb.set_equals_filters(['field_id', 'grouper_id', 'post_id'])
            query = session.query(FieldText).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = FieldTextSchema(many=True)
            return self.handle_success(result, schema, 'get', 'FieldText')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(FieldText).filter_by(id=id).first()
            schema = FieldTextSchema(many=False)
            return self.handle_success(result, schema, 'get_by_id', 'FieldText')

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):
                field_text = FieldText()
                Helper().fill_object_from_data(field_text, data, ['content'])
                self.raise_if_has_different_parent_reference(data, session, [('field_id', 'grouper_id', Field), ('field_id', 'post_id', Field)])
                self.add_foreign_keys(field_text, data, session, [('field_id', Field), ('grouper_id', Grouper), ('post_id', Post)])
                session.add(field_text)
                session.commit()
                return self.handle_success(None, None, 'create', 'FieldText', field_text.id)

            return self.validate_before(process, request.get_json(), FieldTextValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):
                
                def fn(session, field_text):
                    Helper().fill_object_from_data(field_text, data, ['content'])
                    self.raise_if_has_different_parent_reference(data, session, [('field_id', 'grouper_id', Field), ('field_id', 'post_id', Field)])
                    self.add_foreign_keys(field_text, data, session, [('field_id', Field), ('grouper_id', Grouper), ('post_id', Post)])
                    session.commit()
                    return self.handle_success(None, None, 'update', 'FieldText', field_text.id)

                return self.run_if_exists(fn, FieldText, id, session)

            return self.validate_before(process, request.get_json(), FieldTextValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):

            def fn(session, field_text):
                session.delete(field_text)
                session.commit()
                return self.handle_success(None, None, 'delete', 'FieldText', id)

            return self.run_if_exists(fn, FieldText, id, session)

        return self.response(run, True)