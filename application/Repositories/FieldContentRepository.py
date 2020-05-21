from .RepositoryBase import RepositoryBase
from Models import FieldContent, FieldContentSchema, Field, Grouper, Post
from Validators import FieldContentValidator
from Utils import Paginate, ErrorHandler, FilterBuilder

class FieldContentRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of FieldContent."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(FieldContent, args)
            fb.set_like_filter('content')
            fb.set_equals_filter('field_id')
            fb.set_equals_filter('grouper_id')
            fb.set_equals_filter('post_id')

            query = session.query(FieldContent).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = FieldContentSchema(many=True)
            return self.handle_success(result, schema, 'get', 'FieldContent')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(FieldContent).filter_by(id=id).first()
            schema = FieldContentSchema(many=False)
            return self.handle_success(result, schema, 'get_by_id', 'FieldContent')

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):

                field_content = FieldContent(
                    content = data['content']
                )

                can_add_ref = self.forbid_save_with_different_parent_reference(data, session, [('field_id', 'grouper_id', Field), ('field_id', 'post_id', Field)])
                if can_add_ref != True:
                    return can_add_ref

                fk_was_added = self.add_foreign_keys(field_content, data, session, [('field_id', Field), ('grouper_id', Grouper), ('post_id', Post)])
                if fk_was_added != True:
                    return fk_was_added

                session.add(field_content)
                session.commit()
                return self.handle_success(None, None, 'create', 'FieldContent', field_content.id)

            return self.validate_before(process, request.get_json(), FieldContentValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):
                
                def fn(session, field_content):
                    field_content.content = data['content']
                    
                    can_add_ref = self.forbid_save_with_different_parent_reference(data, session, [('field_id', 'grouper_id', Field), ('field_id', 'post_id', Field)])
                    if can_add_ref != True:
                        return can_add_ref

                    fk_was_added = self.add_foreign_keys(field_content, data, session, [('field_id', Field), ('grouper_id', Grouper), ('post_id', Post)])
                    if fk_was_added != True:
                        return fk_was_added
                    
                    session.commit()
                    return self.handle_success(None, None, 'update', 'FieldContent', field_content.id)

                return self.run_if_exists(fn, FieldContent, id, session)

            return self.validate_before(process, request.get_json(), FieldContentValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):

            def fn(session, field_content):
                session.delete(field_content)
                session.commit()
                return self.handle_success(None, None, 'delete', 'FieldContent', id)

            return self.run_if_exists(fn, FieldContent, id, session)

        return self.response(run, True)