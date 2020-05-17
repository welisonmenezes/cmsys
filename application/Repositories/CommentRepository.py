from .RepositoryBase import RepositoryBase
from Models import Comment, CommentSchema
from Validators import CommentValidator
from Utils import Paginate, ErrorHandler, FilterBuilder, Helper

class CommentRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Comment."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(Comment, args)
            # fb.set_equals_filter('type')
            # fb.set_equals_filter('target')
            # fb.set_like_filter('value')

            query = session.query(Comment).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = CommentSchema(many=True)
            return self.handle_success(result, schema, 'get', 'Comment')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(Comment).filter_by(id=id).first()
            schema = CommentSchema(many=False)
            return self.handle_success(result, schema, 'get_by_id', 'Comment')

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):

                comment = Comment(
                    comment = data['comment'],
                    status = data['status'],
                    origin_ip = data['origin_ip'],
                    origin_agent = data['origin_agent'],
                    created = Helper().get_current_datetime(),
                    #parent_id = data['parent_id'],
                    user_id = data['user_id'],
                    post_id = data['post_id'],
                    language_id = data['language_id']
                )
                session.add(comment)
                session.commit()
                return self.handle_success(None, None, 'create', 'Comment', comment.id)

            return self.validate_before(process, request.get_json(), CommentValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):
                
                def fn(session, comment):
                    comment.comment = data['comment']
                    comment.status = data['status']
                    comment.origin_ip = data['origin_ip']
                    comment.origin_agent = data['origin_agent']
                    #comment.parent_id = data['parent_id']
                    comment.user_id = data['user_id']
                    comment.post_id = data['post_id']
                    comment.language_id = data['language_id']
                    session.commit()
                    return self.handle_success(None, None, 'update', 'Comment', comment.id)

                return self.run_if_exists(fn, Comment, id, session)

            return self.validate_before(process, request.get_json(), CommentValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):

            def fn(session, comment):
                session.delete(comment)
                session.commit()
                return self.handle_success(None, None, 'delete', 'Comment', id)

            return self.run_if_exists(fn, Comment, id, session)

        return self.response(run, True)