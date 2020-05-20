from .RepositoryBase import RepositoryBase
from Models import FieldContent, FieldContentSchema
from Validators import FieldContentValidator
from Utils import Paginate, ErrorHandler, FilterBuilder

class FieldContentRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of FieldContent."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):

            # TODO: implement field content filters

            fb = FilterBuilder(FieldContent, args)
            # fb.set_equals_filter('type')
            # fb.set_equals_filter('target')
            # fb.set_like_filter('value')

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
                    content = data['content'],
                    field_id = data['field_id'],
                    grouper_id = data['grouper_id'],
                    post_id = data['post_id']
                )

                # TODO: implement field content relationships
                # TODO: forbid add grouper and post if this ids are different from field

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
                    field_content.field_id = data['field_id']
                    field_content.grouper_id = data['grouper_id']
                    field_content.post_id = data['post_id']
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