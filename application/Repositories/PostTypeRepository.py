from .RepositoryBase import RepositoryBase
from Models import PostType, PostTypeSchema, Template
from Validators import PostTypeValidator
from Utils import Paginate, ErrorHandler, FilterBuilder

class PostTypeRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of PostType."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(PostType, args)
            fb.set_like_filter('name')
            fb.set_equals_filter('type')

            query = session.query(PostType).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = PostTypeSchema(many=True, exclude=self.get_exclude_fields(args, ['template']))
            return self.handle_success(result, schema, 'get', 'PostType')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(PostType).filter_by(id=id).first()
            schema = PostTypeSchema(many=False, exclude=self.get_exclude_fields(args, ['template']))
            return self.handle_success(result, schema, 'get_by_id', 'PostType')

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):

                post_type = PostType(
                    name = data['name'],
                    type = data['type']
                )

                fk_was_added = self.add_foreign_keys(post_type, data, session)
                if (fk_was_added != True):
                    return fk_was_added

                session.add(post_type)
                session.commit()
                return self.handle_success(None, None, 'create', 'PostType', post_type.id)

            return self.validate_before(process, request.get_json(), PostTypeValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):
                post_type = session.query(PostType).filter_by(id=id).first()

                if (post_type):
                    post_type.name = data['name']
                    post_type.type = data['type']

                    fk_was_added = self.add_foreign_keys(post_type, data, session)
                    if (fk_was_added != True):
                        return fk_was_added

                    session.commit()
                    return self.handle_success(None, None, 'update', 'PostType', post_type.id)

                else:
                    return ErrorHandler().get_error(404, 'No PostType found.')

            return self.validate_before(process, request.get_json(), PostTypeValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):
            post_type = session.query(PostType).filter_by(id=id).first()

            if post_type:

                # TODO: forbid delete post type witch has a related post

                session.delete(post_type)
                session.commit()
                return self.handle_success(None, None, 'delete', 'PostType', id)

            else:
                return ErrorHandler().get_error(404, 'No PostType found.')

        return self.response(run, True)


    def add_foreign_keys(self, post_type, data, session):
        """Controls if the template_id is an existing foreign key data."""

        try:
            post_type.template_id = self.get_existing_foreing_id(data, 'template_id', Template, session)
            return True
        except Exception as e:
            return ErrorHandler().get_error(400, e)