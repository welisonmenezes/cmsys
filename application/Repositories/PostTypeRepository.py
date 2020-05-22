from .RepositoryBase import RepositoryBase
from Models import PostType, PostTypeSchema, Template, Post, Nest
from Validators import PostTypeValidator
from Utils import Paginate, FilterBuilder, Helper

class PostTypeRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of PostType."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(PostType, args)
            fb.set_like_filters(['name'])
            fb.set_equals_filters(['type'])
            query = session.query(PostType).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = PostTypeSchema(many=True, exclude=self.get_exclude_fields(args, ['template', 'nests']))
            return self.handle_success(result, schema, 'get', 'PostType')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(PostType).filter_by(id=id).first()
            schema = PostTypeSchema(many=False, exclude=self.get_exclude_fields(args, ['template', 'nests']))
            return self.handle_success(result, schema, 'get_by_id', 'PostType')

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):
                post_type = PostType()
                Helper().fill_object_from_data(post_type, data, ['name', 'type'])
                self.add_foreign_keys(post_type, data, session, [('template_id', Template)])
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

                def fn(session, post_type):
                    Helper().fill_object_from_data(post_type, data, ['name', 'type'])
                    self.add_foreign_keys(post_type, data, session, [('template_id', Template)])
                    session.commit()
                    return self.handle_success(None, None, 'update', 'PostType', post_type.id)

                return self.run_if_exists(fn, PostType, id, session)

            return self.validate_before(process, request.get_json(), PostTypeValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):

            def fn(session, post_type):
                self.is_foreigners([(post_type, 'post_type_id', Post)], session)
                session.query(Nest).filter_by(post_type_id=post_type.id).delete(synchronize_session='evaluate')
                session.delete(post_type)
                session.commit()
                return self.handle_success(None, None, 'delete', 'PostType', id)

            return self.run_if_exists(fn, PostType, id, session)

        return self.response(run, True)