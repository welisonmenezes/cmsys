from .RepositoryBase import RepositoryBase
from Models import Field, FieldSchema
from Validators import FieldValidator
from Utils import Paginate, ErrorHandler, FilterBuilder

class FieldRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Field."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(Field, args)
            fb.set_equals_filter('type')
            fb.set_equals_filter('grouper_id')
            fb.set_equals_filter('post_id')

            try:
                fb.set_and_or_filter('s', 'or', [{'field':'name', 'type':'like'}, {'field':'description', 'type':'like'}])
            except Exception as e:
                return ErrorHandler().get_error(400, str(e))

            query = session.query(Field).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = FieldSchema(many=True, exclude=self.get_exclude_fields(args, ['post', 'grouper']))
            return self.handle_success(result, schema, 'get', 'Field')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(Field).filter_by(id=id).first()
            schema = FieldSchema(many=False, exclude=self.get_exclude_fields(args, ['post', 'grouper']))
            return self.handle_success(result, schema, 'get_by_id', 'Field')

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):

                field = Field(
                    name = data['name'],
                    description = data['description'],
                    type = data['type'],
                    order = data['order'],
                    grouper_id = data['grouper_id'],
                    post_id = data['post_id']
                )

                # TODO: implement the Field relationships transformations

                session.add(field)
                session.commit()
                return self.handle_success(None, None, 'create', 'Field', field.id)

            return self.validate_before(process, request.get_json(), FieldValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):
                
                def fn(session, field):
                    field.name = data['name']
                    field.description = data['description']
                    field.type = data['type']
                    field.order = data['order']
                    field.grouper_id = data['grouper_id']
                    field.post_id = data['post_id']

                    # TODO: when the type of a Fild was changed, delete its related child

                    session.commit()
                    return self.handle_success(None, None, 'update', 'Field', field.id)

                return self.run_if_exists(fn, Field, id, session)

            return self.validate_before(process, request.get_json(), FieldValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):

            def fn(session, field):

                # TODO: when to delete a Field, delete also its children (text, content or file)

                session.delete(field)
                session.commit()
                return self.handle_success(None, None, 'delete', 'Field', id)

            return self.run_if_exists(fn, Field, id, session)

        return self.response(run, True)