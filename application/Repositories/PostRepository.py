from .RepositoryBase import RepositoryBase
from Models import Post, PostSchema, PostType, Language, User, Nest, Comment, FieldContent, FieldText, FieldFile, Field, Grouper, Term
from Validators import PostValidator, GrouperValidator, FieldValidator, FieldContentValidator, FieldTextValidator, FieldFileValidator
from Utils import Paginate, FilterBuilder, Helper, Checker
from ErrorHandlers import BadRequestError

# TODO: from post to be able to save/update/delete grouper and fields

class PostRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Post."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

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

                # change when access control was working
                is_logged = True
                if not is_logged:
                    fb.set_range_of_dates_filter()

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
            result = self.get_result_by_unique_key(id, Post, session)
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
                post = Post()
                Helper().fill_object_from_data(post, data, ['name', 'title', 'description', 'status', 'is_protected', 'has_comments'])
                post.publish_on = Helper().get_null_if_empty(data['publish_on'])
                post.expire_on = Helper().get_null_if_empty(data['expire_on'])
                post.created = Helper().get_current_datetime()
                post.edited = Helper().get_current_datetime()
                self.add_foreign_keys(post, data, session, [('parent_id', Post), ('post_type_id', PostType), ('language_id', Language), ('user_id', User)])
                self.raise_if_has_term_and_not_is_post_page(data, session)
                self.add_many_to_many_relationship('terms', post, data, Term, session)
                
                session.add(post)
                self.save_groupers_into_post(data, post, session)

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
                    self.raise_if_has_term_and_not_is_post_page(data, session)
                    self.edit_many_to_many_relationship('terms', post, data, Term, session)

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


    def raise_if_has_term_and_not_is_post_page(self, data, session):
        """Raise an error if the Post has terms but it does not is from a Post_Type with type 'post-page'"""

        if 'terms' in data and data['terms']:
            if 'post_type_id' in data and Checker().can_be_integer(data['post_type_id']):
                post_type = session.query(PostType.type).filter_by(id=int(data['post_type_id'])).first()
                if post_type and post_type[0]:
                    if post_type[0] != 'post-page':
                        raise BadRequestError('The Post_Type of the Post must be settled as type \'post-page\' to have Terms.')



    def save_groupers_into_post(self, data, post, session, parent_id=None):
        """"""
        session.flush()
        errors = []
        if 'groupers' in data and isinstance(data['groupers'], list) and len(data['groupers']) > 0:
           
            for grouper in data['groupers']:

                pgrouper_id = parent_id

                if len(grouper) > 0:
                    
                    grouper['post_id'] = post.id
                    if pgrouper_id:
                        grouper['parent_id'] = pgrouper_id
                    grouper_validator = GrouperValidator(grouper)

                    if grouper_validator.is_valid():

                        new_grouper = Grouper()
                        Helper().fill_object_from_data(new_grouper, grouper, ['name', 'description', 'order', 'parent_id'])
                        post.groupers.append(new_grouper)
                        self.save_fields_into_grouper(grouper, post, new_grouper, session)
                        pgrouper_id = new_grouper.id
                        
                    else:
                        raise BadRequestError(grouper_validator.get_errors())

                    self.save_groupers_into_post(grouper, post, session, pgrouper_id)


    def save_fields_into_grouper(self, data, post, grouper, session):
        """"""

        session.flush()
        errors = []
        if 'fields' in data and isinstance(data['fields'], list) and len(data['fields']) > 0:

            for field in data['fields']:
                
                field['grouper_id'] = grouper.id
                field['post_id'] = post.id
                field_validator = FieldValidator(field)
                
                if field_validator.is_valid():

                    new_field = Field()
                    Helper().fill_object_from_data(new_field, field, ['name', 'description', 'type', 'order', 'grouper_id', 'post_id'])
                    grouper.fields.append(new_field)

                    if new_field.type == 'long-text':
                        self.save_field_content_into_field(field, post, grouper, new_field, session)

                    elif new_field.type == 'short-text':
                        self.save_field_text_into_field(field, post, grouper, new_field, session)

                    elif new_field.type == 'file':
                        self.save_field_file_into_field(field, post, grouper, new_field, session)
                    
                else:
                    raise BadRequestError(field_validator.get_errors())

                self.save_fields_into_grouper(field, post, grouper, session)


    def save_field_content_into_field(self, data, post, grouper, field, session):
        """"""

        session.flush()
        errors = []
        if 'field' in data and data['field'] != '':

            field_content = data['field']
            field_content['grouper_id'] = grouper.id
            field_content['post_id'] = post.id
            field_content['field_id'] = field.id
            field_validator = FieldContentValidator(field_content)

            if field_validator.is_valid():

                    new_field = FieldContent()
                    Helper().fill_object_from_data(new_field, field_content, ['content', 'post_id', 'grouper_id', 'field_id'])
                    session.add(new_field)
                    
            else:
                raise BadRequestError(field_validator.get_errors())



    def save_field_text_into_field(self, data, post, grouper, field, session):
        """"""

        session.flush()
        errors = []
        if 'field' in data and data['field'] != '':

            field_text = data['field']
            field_text['grouper_id'] = grouper.id
            field_text['post_id'] = post.id
            field_text['field_id'] = field.id
            field_validator = FieldTextValidator(field_text)

            if field_validator.is_valid():

                    new_field = FieldText()
                    Helper().fill_object_from_data(new_field, field_text, ['content', 'post_id', 'grouper_id', 'field_id'])
                    session.add(new_field)
                    
            else:
                raise BadRequestError(field_validator.get_errors())

    
    def save_field_file_into_field(self, data, post, grouper, field, session):
        """"""

        session.flush()
        errors = []
        if 'field' in data and data['field'] != '':

            field_file = data['field']
            field_file['grouper_id'] = grouper.id
            field_file['post_id'] = post.id
            field_file['field_id'] = field.id
            field_validator = FieldFileValidator(field_file)

            if field_validator.is_valid():

                    new_field = FieldFile()
                    Helper().fill_object_from_data(new_field, field_file, ['media_id', 'post_id', 'grouper_id', 'field_id'])
                    session.add(new_field)
                    
            else:
                raise BadRequestError(field_validator.get_errors())