from .RepositoryBase import RepositoryBase
from Models import Post, PostSchema, PostType, Language, User
from Validators import PostValidator
from Utils import Paginate, ErrorHandler, FilterBuilder, Helper

class PostRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Post."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

            # TODO: implement the post publish_on and expire_on filters
            # TODO: filter by child field

        def run(session):
            fb = FilterBuilder(Post, args)
            fb.set_equals_filter('status')
            fb.set_equals_filter('user_id')
            fb.set_equals_filter('parent_id')
            fb.set_equals_filter('post_type_id')
            fb.set_equals_filter('language_id')

            try:
                fb.set_date_filter('created', date_modifier=args['date_modifier'])
                fb.set_between_dates_filter(
                    'created',
                    compare_date_time_one=args['compare_date_time_one'],
                    compare_date_time_two=args['compare_date_time_two'],
                    not_between=args['not_between']
                )
                fb.set_and_or_filter('s', 'or', [{'field':'name', 'type':'like'}, {'field':'title', 'type':'like'}, {'field':'description', 'type':'like'}])
            except Exception as e:
                return ErrorHandler().get_error(400, str(e))

            query = session.query(Post).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = PostSchema(many=True, exclude=self.get_exclude_fields(args, ['user', 'language']))
            return self.handle_success(result, schema, 'get', 'Post')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(Post).filter_by(id=id).first()
            schema = PostSchema(many=False, exclude=self.get_exclude_fields(args, ['user', 'language']))
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

                post = Post(
                    name = data['name'],
                    title = data['title'],
                    description = data['description'],
                    status = data['status'],
                    is_protected = data['is_protected'],
                    has_comments = data['has_comments'],
                    publish_on = Helper().get_null_if_empty(data['publish_on']),
                    expire_on = Helper().get_null_if_empty(data['expire_on']),
                    created = Helper().get_current_datetime(),
                    edited = Helper().get_current_datetime()
                )

                fk_was_added = self.add_foreign_keys(post, data, session, [('parent_id', Post), ('post_type_id', PostType), ('language_id', Language), ('user_id', User)])
                if fk_was_added != True:
                    return fk_was_added

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
                    post.name = data['name']
                    post.title = data['title']
                    post.description = data['description']
                    post.status = data['status']
                    post.is_protected = data['is_protected']
                    post.has_comments = data['has_comments']
                    post.publish_on = Helper().get_null_if_empty(data['publish_on'])
                    post.expire_on = Helper().get_null_if_empty(data['expire_on'])
                    post.edited = Helper().get_current_datetime()

                    fk_was_added = self.add_foreign_keys(post, data, session, [('parent_id', Post), ('post_type_id', PostType), ('language_id', Language), ('user_id', User)])
                    if fk_was_added != True:
                        return fk_was_added

                    session.commit()
                    return self.handle_success(None, None, 'update', 'Post', post.id)

                return self.run_if_exists(fn, Post, id, session)

            return self.validate_before(process, Helper().get_with_slug(request.get_json(), 'name'), PostValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):

            def fn(session, post):

                # TODO: forbid delete post that has Nested Post
                # TODO: forbid delete post that is term page (or update the term page)
                # TODO: forbid delete post that has comments (or delete its comments)

                can_delete = self.set_foreign_keys_as_null(post, request, session, [('page_id', User), ('parent_id', Post)])
                if can_delete != True:
                    return can_delete

                session.delete(post)
                session.commit()
                return self.handle_success(None, None, 'delete', 'Post', id)

            return self.run_if_exists(fn, Post, id, session)

        return self.response(run, True)


    def add_foreign_keys(self, current_context, data, session, configurations):
        """Controls if the list of foreign keys is an existing foreign key data. How to use:
            The configurtations must like: [('foreign_key_at_target_context, target_context)]"""

        errors = []
        for config in configurations:
            try:
                if config[0] == 'parent_id':
                    """If the post referenced by the parent_id is not post_type of type post-page, return error."""

                    el = self.get_existing_foreing_id(data, config[0], config[1], session, True)
                    if el and el.post_type and el.post_type.type != 'post-page':
                        errors.append('The Post_Type \'' + el.post_type.name + '\' of the parent post is \'' + el.post_type.type + '\' It must be \'post-page\'.')
                        continue

                setattr(current_context, config[0], self.get_existing_foreing_id(data, config[0], config[1], session))

            except Exception as e:
                errors.append(str(e))
                
        return True if not errors else ErrorHandler().get_error(400, errors)


    def set_foreign_keys_as_null(self, instance, request, session, configurations):
        """Sets the given foreign key at the given Model as None to allow delete the given instance.
            Note that this only occurs if the 'remove_foreign_key' passed by request param was equals 1.
            How to use: The configuration must like: [(foreign_key_at_target_context, target_context)]"""

        errors = []
        for config in configurations:
            try:
                    if 'remove_foreign_keys' in request.args and request.args['remove_foreign_keys'] == '1':
                        filter = (getattr(config[1], config[0])==instance.id,)
                        elements = session.query(config[1]).filter(*filter).all()
                        for element in elements:
                            setattr(element, config[0], None)
                    else:
                        filter = (getattr(config[1], config[0])==instance.id,)
                        element = session.query(getattr(config[1], 'id')).filter(*filter).first()
                        if element:
                            errors.append('You cannot delete this ' + instance.__class__.__name__ + ' because it has a related ' + config[1].__tablename__)

            except Exception as e:
                errors.append(str(e))
                
        return True if not errors else ErrorHandler().get_error(400, errors)
        