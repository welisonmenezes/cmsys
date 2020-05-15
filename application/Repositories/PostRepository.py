from .RepositoryBase import RepositoryBase
from Models import Post, PostSchema
from Validators import PostValidator
from Utils import Paginate, ErrorHandler, FilterBuilder

class PostRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Post."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(Post, args)
            # fb.set_equals_filter('type')
            # fb.set_equals_filter('target')
            # fb.set_like_filter('value')

            query = session.query(Post).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = PostSchema(many=True)
            return self.handle_success(result, schema, 'get', 'Post')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(Post).filter_by(id=id).first()
            schema = PostSchema(many=False)
            return self.handle_success(result, schema, 'get_by_id', 'Post')

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):

                post = Post(
                    name = data['name'],
                    title = data['title'],
                    description = data['description'],
                    status = data['status'],
                    is_protected = data['is_protected'],
                    has_comments = data['has_comments'],
                    #publish_on = data['publish_on'],
                    #expire_on = data['expire_on'],
                    #parent_id = data['parent_id'],
                    post_type_id = data['post_type_id'],
                    language_id = data['language_id'],
                    user_id = data['user_id']
                )
                session.add(post)
                session.commit()
                return self.handle_success(None, None, 'create', 'Post', post.id)

            return self.validate_before(process, request.get_json(), PostValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):
                
                def fn(session, post):
                    post.name = data['name']
                    post.title = data['title']
                    post.description = data['description']
                    post.status = data['status']
                    post.is_protected = data['is_protected']
                    post.has_comments = data['has_comments']
                    #post.publish_on = data['publish_on']
                    #post.expire_on = data['expire_on']
                    #post.parent_id = data['parent_id']
                    post.post_type_id = data['post_type_id']
                    post.language_id = data['language_id']
                    post.user_id = data['user_id']
                    session.commit()
                    return self.handle_success(None, None, 'update', 'Post', post.id)

                return self.run_if_exists(fn, Post, id, session)

            return self.validate_before(process, request.get_json(), PostValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):

            def fn(session, post):
                session.delete(post)
                session.commit()
                return self.handle_success(None, None, 'delete', 'Post', id)

            return self.run_if_exists(fn, Post, id, session)

        return self.response(run, True)