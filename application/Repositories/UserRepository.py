from app import bcrypt
from .RepositoryBase import RepositoryBase
from Models import User, UserSchema, Media, Post, Role, Social, Comment
from Validators import UserValidator
from Utils import Paginate, FilterBuilder, Helper, Checker
from ErrorHandlers import BadRequestError, NotFoundError

# TODO: from user to be able to save/update/delete socials

class UserRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of User."""

    def __init__(self, session):
        super().__init__(session)
        

    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        fb = FilterBuilder(User, args)
        fb.set_like_filters(['email'])
        fb.set_equals_filters(['status', 'role_id'])

        try:
            fb.set_date_filter('registered', date_modifier=args['date_modifier'])
            fb.set_between_dates_filter(
                'registered', not_between=args['not_between'],
                compare_date_time_one=args['compare_date_time_one'],
                compare_date_time_two=args['compare_date_time_two']
            )
            fb.set_and_or_filter('s', 'or', [{'field':'first_name', 'type':'like'}, {'field':'last_name', 'type':'like'}, {'field':'nickname', 'type':'like'}])
        except Exception as e:
            raise BadRequestError(str(e))

        query = self.session.query(User).filter(*fb.get_filter()).order_by(*fb.get_order_by())
        result = Paginate(query, fb.get_page(), fb.get_limit())
        excluded_fields = self.get_exclude_fields(args, ['role', 'socials', 'medias', 'page', 'avatar'])
        excluded_fields += ('password', 'refresh_token',)
        schema = UserSchema(many=True, exclude=excluded_fields)
        return self.handle_success(result, schema, 'get', 'User')
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        result = self.session.query(User).filter_by(id=id).first()
        excluded_fields = self.get_exclude_fields(args, ['role', 'socials', 'medias', 'page', 'avatar'])
        excluded_fields += ('password', 'refresh_token',)
        schema = UserSchema(many=False, exclude=excluded_fields)
        return self.handle_success(result, schema, 'get_by_id', 'User')

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def process(session, data):
            user = User()
            Helper().fill_object_from_data(user, data, ['login', 'nickname', 'first_name', 'last_name', 'email', 'status'])
            user.password = bcrypt.generate_password_hash(data['password'])
            user.registered = Helper().get_current_datetime()
            self.add_foreign_keys(user, data, session, [('role_id', Role), ('page_id', Post), ('avatar_id', Media)])
            session.add(user)
            session.commit()
            return self.handle_success(None, None, 'create', 'User', user.id)

        return self.validate_before(process, request.get_json(), UserValidator, self.session)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def process(session, data):

            def fn(session, user):
                Helper().fill_object_from_data(user, data, ['login', 'nickname', 'first_name', 'last_name', 'email', 'status'])

                if data['password'] != '' and not bcrypt.check_password_hash(user.password, data['password']):
                    user.password = bcrypt.generate_password_hash(data['password'])

                self.add_foreign_keys(user, data, session, [('role_id', Role), ('page_id', Post), ('avatar_id', Media)])
                session.commit()
                return self.handle_success(None, None, 'update', 'User', user.id)

            return self.run_if_exists(fn, User, id, session)

        return self.validate_before(process, request.get_json(), UserValidator, self.session, id=id)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        if id == 1:
            raise BadRequestError('The Super Admin user cannot be deleted.')

        def fn(session, user):
            self.delegate_content_to_delete(user,session, request, (Media, Post))
            self.delete_user_comments(user, session)
            self.delete_children(session, id, [('user_id', Social)])
            session.delete(user)
            session.commit()
            return self.handle_success(None, None, 'delete', 'User', id)

        return self.run_if_exists(fn, User, id, self.session)


    def add_foreign_keys(self, current_context, data, session, configurations):
        """Controls if the list of foreign keys is an existing foreign key data. How to use:
            The configurtations must like: [('foreign_key_at_target_context, target_context)]"""

        for config in configurations:
            try:
                if getattr(current_context, 'id') == 1 and config[0] == 'role_id':
                    raise BadRequestError('You cannot change the role of the primary user admin.')

                if config[0] == 'avatar_id' and config[0] in data:
                    image = self.get_existing_foreing_id(data, 'avatar_id', Media, session, True)
                    if not image or not Checker().is_image_type(image.type):
                        raise BadRequestError('The user avatar must be an image file.')

                if config[0] == 'page_id':
                    """If the post referenced by the page_id is not post_type of type user-profile, return error."""

                    el = self.get_existing_foreing_id(data, config[0], config[1], session, True)
                    if el and el.post_type and el.post_type.type != 'user-profile':
                        raise BadRequestError('The Post_Type \'' + el.post_type.name + '\' of the parent post is \'' + el.post_type.type + '\' It must be \'user-profile\'.')
                
                setattr(current_context, config[0], self.get_existing_foreing_id(data, config[0], config[1], session))

            except Exception as e:
                raise BadRequestError(str(e))


    def delegate_content_to_delete(self, user, session, request, context_list):
        """Delegates user's contents to superadmin (id=1) from list of context passed 
            by parameter context_list. Only do that if admin_new_owner is given as arg"""

        for content_context in context_list:
            content = session.query(content_context).filter_by(user_id=user.id).first()
            if content:
                if 'admin_new_owner' in request.args and request.args['admin_new_owner'] == '1':
                    contents = session.query(content_context).filter_by(user_id=user.id).all()
                    for c in contents:
                        admin = session.query(User).filter_by(id=1).first()
                        if admin:
                            c.user_id = admin.id
                        else:
                            raise NotFoundError('Could not find the super admin user.')
                else:
                    raise BadRequestError('You cannot delete this User because it has related ' + content_context.__tablename__ + '.')


    def delete_user_comments(self, user, session):
        """Delete the user comments."""

        comment = session.query(Comment.id).filter_by(user_id=user.id).first()
        if comment:
            comments = session.query(Comment).filter_by(user_id=user.id).all()
            for comm in comments:
                self.set_children_as_null_to_delete(comm, Comment, session)
                session.delete(comm)