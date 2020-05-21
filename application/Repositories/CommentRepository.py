from .RepositoryBase import RepositoryBase
from Models import Comment, CommentSchema, User, Post, Language
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
            fb.set_like_filters(['comment', 'origin_ip', 'origin_agent'])
            fb.set_equals_filters(['status', 'parent_id', 'user_id', 'post_id', 'language_id'])
            
            try:
                fb.set_date_filter('created', date_modifier=args['date_modifier'])
                fb.set_between_dates_filter(
                    'created',  not_between=args['not_between'],
                    compare_date_time_one=args['compare_date_time_one'],
                    compare_date_time_two=args['compare_date_time_two']
                )
            except Exception as e:
                return ErrorHandler().get_error(400, str(e))

            query = session.query(Comment).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = CommentSchema(many=True, exclude=self.get_exclude_fields(args, ['user', 'language', 'parent', 'children', 'post']))
            return self.handle_success(result, schema, 'get', 'Comment')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(Comment).filter_by(id=id).first()
            schema = CommentSchema(many=False, exclude=self.get_exclude_fields(args, ['user', 'language', 'parent', 'children', 'post']))
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
                    created = Helper().get_current_datetime()
                )
                self.raise_if_has_different_parent_reference(data, session, [('parent_id', 'post_id', Comment), ('parent_id', 'language_id', Comment)])
                self.add_foreign_keys(comment, data, session, [('user_id', User), ('post_id', Post), ('language_id', Language), ('parent_id', Comment)])
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
                    self.raise_if_has_different_parent_reference(data, session, [('parent_id', 'post_id', Comment), ('parent_id', 'language_id', Comment)])
                    self.add_foreign_keys(comment, data, session, [('user_id', User), ('post_id', Post), ('language_id', Language), ('parent_id', Comment)])
                    
                    if comment.parent_id and int(comment.parent_id) == int(id):
                        return ErrorHandler().get_error(400, 'The Comment cannot be parent of yourself.')

                    session.commit()
                    return self.handle_success(None, None, 'update', 'Comment', comment.id)

                return self.run_if_exists(fn, Comment, id, session)

            return self.validate_before(process, request.get_json(), CommentValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):

            def fn(session, comment):
                self.set_children_as_null_to_delete(comment, Comment, session)
                session.delete(comment)
                session.commit()
                return self.handle_success(None, None, 'delete', 'Comment', id)

            return self.run_if_exists(fn, Comment, id, session)

        return self.response(run, True)