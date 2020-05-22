from .RepositoryBase import RepositoryBase
from Models import FieldContent, FieldContentSchema, Field, Grouper, Post
from Validators import FieldContentValidator
from Utils import Paginate, FilterBuilder, Helper
from ErrorHandlers import BadRequestError

# TODO: forbid save new field type if already exists any ohter at the specified field

class FieldContentRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of FieldContent."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(FieldContent, args)
            fb.set_like_filters(['content'])
            fb.set_equals_filters(['field_id', 'grouper_id', 'post_id'])
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
                field_content = FieldContent()
                Helper().fill_object_from_data(field_content, data, ['content'])
                self.raise_if_has_different_parent_reference(data, session, [('field_id', 'grouper_id', Field), ('field_id', 'post_id', Field)])
                self.add_foreign_keys(field_content, data, session, [('field_id', Field), ('grouper_id', Grouper), ('post_id', Post)])
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
                    Helper().fill_object_from_data(field_content, data, ['content'])
                    self.raise_if_has_different_parent_reference(data, session, [('field_id', 'grouper_id', Field), ('field_id', 'post_id', Field)])
                    self.add_foreign_keys(field_content, data, session, [('field_id', Field), ('grouper_id', Grouper), ('post_id', Post)])
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


    def add_foreign_keys(self, current_context, data, session, configurations):
        """Controls if the list of foreign keys is an existing foreign key data. How to use:
            The configurtations must like: [('foreign_key_at_target_context, target_context)]"""

        errors = []
        for config in configurations:
            try:
                if config[0] == 'field_id':
                    el = self.get_existing_foreing_id(data, config[0], config[1], session, True)
                    if el and el.type != 'long-text':
                        errors.append('The Field referenced by the \'field_id\' is not configured as long-text.')

                setattr(current_context, config[0], self.get_existing_foreing_id(data, config[0], config[1], session))
            except Exception as e:
                errors.append('Could not find the given foreign key \'' + str(config[0]) + '\'')

        if errors:
            raise BadRequestError(errors)