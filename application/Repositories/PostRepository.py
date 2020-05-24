from .RepositoryBase import RepositoryBase
from Models import Post, PostSchema, PostType, Language, User, Nest, Comment, FieldContent, FieldText, FieldFile, Field, Grouper, Term
from Validators import PostValidator
from Utils import Paginate, FilterBuilder, Helper, Checker
from ErrorHandlers import BadRequestError

# TODO: from post to be able to save/update/delete grouper and fields

class PostRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Post."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        # TODO: implement the post publish_on and expire_on filters

        def run(session):
            fb = FilterBuilder(Post, args)
            fb.set_equals_filters(['status', 'user_id', 'parent_id', 'post_type_id', 'language_id'])
            self.joins.append(FieldContent)
            self.joins.append(FieldText)

            if (args['term_id'] and args['term_id'] != '' and Checker().can_be_integer(args['term_id'])):
                fb.set_like_filter('term_id', joined=Term, joined_key='id')
                self.joins.append(Post.terms)

            try:
                fb.set_date_filter('created', date_modifier=args['date_modifier'])
                fb.set_between_dates_filter(
                    'created', not_between=args['not_between'],
                    compare_date_time_one=args['compare_date_time_one'],
                    compare_date_time_two=args['compare_date_time_two']
                )
                fb.set_and_or_filter('s', 'or', [
                    {'field': 'name', 'type': 'like'},
                    {'field': 'title', 'type': 'like'},
                    {'field': 'description', 'type': 'like'},
                    {'field': 'content', 'type': 'like', 'kwargs': {'joined': FieldContent}},
                    {'field': 'content', 'type': 'like', 'kwargs': {'joined': FieldText}}
                ])
            except Exception as e:
                raise BadRequestError(str(e))

            query = session.query(Post).join(*self.joins, isouter=True).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = PostSchema(many=True, exclude=self.get_exclude_fields(args, [
                'user', 'language', 'parent', 'children', 'post_type', 'nests', 'groupers', 'terms']))
            return self.handle_success(result, schema, 'get', 'Post')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(Post).filter_by(id=id).first()
            schema = PostSchema(many=False, exclude=self.get_exclude_fields(args, [
                'user', 'language', 'parent', 'children', 'post_type', 'nests', 'groupers', 'terms']))
            return self.handle_success(result, schema, 'get_by_id', 'Post')

        return self.response(run, False)


    def get_name_suggestions(self, name, args):
        """Returns names suggestions to new Media."""

        def run(session):
            return self.get_suggestions(name, Post, session)

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):
            
            def process(session, data):

                # The child post_type must be equals the parent post type
                # TODO: implement the Post relationships Term

                post = Post()
                Helper().fill_object_from_data(post, data, ['name', 'title', 'description', 'status', 'is_protected', 'has_comments'])
                post.publish_on = Helper().get_null_if_empty(data['publish_on'])
                post.expire_on = Helper().get_null_if_empty(data['expire_on'])
                post.created = Helper().get_current_datetime()
                post.edited = Helper().get_current_datetime()
                self.add_foreign_keys(post, data, session, [('parent_id', Post), ('post_type_id', PostType), ('language_id', Language), ('user_id', User)])
                session.add(post)
                session.commit()
                return self.handle_success(None, None, 'create', 'Post', post.id)

            return self.validate_before(process, Helper().get_with_slug(request.get_json(), 'name'), PostValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""
        
        def run(session):
            
            def process(session, data):
                
                def fn(session, post):
                    Helper().fill_object_from_data(post, data, ['name', 'title', 'description', 'status', 'is_protected', 'has_comments'])
                    post.publish_on = Helper().get_null_if_empty(data['publish_on'])
                    post.expire_on = Helper().get_null_if_empty(data['expire_on'])
                    post.edited = Helper().get_current_datetime()
                    self.add_foreign_keys(post, data, session, [('parent_id', Post), ('post_type_id', PostType), ('language_id', Language), ('user_id', User)])

                    if post.parent_id and int(post.parent_id) == int(id):
                        raise BadRequestError('The Post cannot be parent of yourself.')

                    session.commit()
                    return self.handle_success(None, None, 'update', 'Post', post.id)

                return self.run_if_exists(fn, Post, id, session)

            return self.validate_before(process, Helper().get_with_slug(request.get_json(), 'name'), PostValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):

            def fn(session, post):
                self.set_any_reference_as_null_to_delete(post, request, session, [('page_id', User), ('parent_id', Post)])
                self.delete_children(session, id, [
                    ('post_id', Comment), ('post_id', Nest),
                    ('post_id', FieldContent), ('post_id', FieldFile), ('post_id', FieldText), 
                    ('post_id', Field), ('post_id', Grouper)
                ])
                session.delete(post)
                session.commit()
                return self.handle_success(None, None, 'delete', 'Post', id)

            return self.run_if_exists(fn, Post, id, session)

        return self.response(run, True)


    def add_foreign_keys(self, current_context, data, session, configurations):
        """Controls if the list of foreign keys is an existing foreign key data. How to use:
            The configurtations must like: [('foreign_key_at_target_context, target_context)]"""

        for config in configurations:
            try:
                if config[0] == 'parent_id':
                    """If the post referenced by the parent_id is not post_type of type post-page, return error."""

                    el = self.get_existing_foreing_id(data, config[0], config[1], session, True)
                    if el and el.post_type and el.post_type.type != 'post-page':
                        raise BadRequestError('The Post_Type \'' + el.post_type.name + '\' of the parent post is \'' + el.post_type.type + '\' It must be \'post-page\'.')

                setattr(current_context, config[0], self.get_existing_foreing_id(data, config[0], config[1], session))

            except Exception as e:
                raise BadRequestError(str(e))