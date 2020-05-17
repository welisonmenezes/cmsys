from app import bcrypt
from .RepositoryBase import RepositoryBase
from Models import User, UserSchema, Media, Post, Role, Social
from Validators import UserValidator
from Utils import Paginate, ErrorHandler, FilterBuilder, Helper, Checker


class UserRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of User."""

    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(User, args)
            fb.set_like_filter('email')
            fb.set_equals_filter('status')
            fb.set_equals_filter('role_id')

            try:
                fb.set_date_filter('registered', date_modifier=args['date_modifier'])
                fb.set_between_dates_filter(
                    'registered',
                    compare_date_time_one=args['compare_date_time_one'],
                    compare_date_time_two=args['compare_date_time_two'],
                    not_between=args['not_between']
                )
                fb.set_and_or_filter('s', 'or', [{'field':'first_name', 'type':'like'}, {'field':'last_name', 'type':'like'}, {'field':'nickname', 'type':'like'}])
            except Exception as e:
                return ErrorHandler().get_error(400, str(e))

            query = session.query(User).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            excluded_fields = self.get_exclude_fields(args, ['role', 'socials', 'medias', 'page', 'avatar'])
            excluded_fields += ('password',)
            schema = UserSchema(many=True, exclude=excluded_fields)
            return self.handle_success(result, schema, 'get', 'User')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(User).filter_by(id=id).first()
            excluded_fields = self.get_exclude_fields(args, ['role', 'socials', 'medias', 'page', 'avatar'])
            excluded_fields += ('password',)
            schema = UserSchema(many=False, exclude=excluded_fields)
            return self.handle_success(result, schema, 'get_by_id', 'User')

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):
                user = User(
                    login = data['login'],
                    password = bcrypt.generate_password_hash(data['password']),
                    nickname = data['nickname'],
                    first_name = data['first_name'],
                    last_name = data['last_name'],
                    email = data['email'],
                    status = data['status'],
                    registered = Helper().get_current_datetime()
                )
                
                fk_was_added = self.add_foreign_keys(user, data, session, [('role_id', Role), ('page_id', Post), ('avatar_id', Media)])
                if fk_was_added != True:
                    return fk_was_added

                session.add(user)
                session.commit()
                return self.handle_success(None, None, 'create', 'User', user.id)

            return self.validate_before(process, request.get_json(), UserValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):

                def fn(session, user):
                    user.login = data['login']
                    user.nickname = data['nickname']
                    user.first_name = data['first_name']
                    user.last_name = data['last_name']
                    user.email = data['email']
                    user.status = data['status']
                    user.registered = Helper().get_current_datetime()

                    if data['password'] != '' and not bcrypt.check_password_hash(user.password, data['password']):
                        user.password = bcrypt.generate_password_hash(data['password'])

                    fk_was_added = self.add_foreign_keys(user, data, session, [('role_id', Role), ('page_id', Post), ('avatar_id', Media)])
                    if fk_was_added != True:
                        return fk_was_added

                    session.commit()
                    return self.handle_success(None, None, 'update', 'User', user.id)

                return self.run_if_exists(fn, User, id, session)

            return self.validate_before(process, request.get_json(), UserValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        if id == 1:
            return ErrorHandler().get_error(400, 'The Super Admin user cannot be deleted.')

        def run(session):

            def fn(session, user):
                
                # TODO: check if user has comments (delete comments and sets the children as no parent)

                image_was_deleted = self.delegate_content_to_delete(user,session, request, (Media, Post))
                if image_was_deleted != True:
                    return image_was_deleted

                session.query(Social).filter_by(user_id=user.id).delete(synchronize_session='evaluate')

                session.delete(user)
                session.commit()
                return self.handle_success(None, None, 'delete', 'User', id)

            return self.run_if_exists(fn, User, id, session)

        return self.response(run, True)


    def add_foreign_keys(self, current_context, data, session, configurations):
        """Controls if the list of foreign keys is an existing foreign key data. How to use:
            The configurtations must like: [('foreign_key_at_target_context, target_context)]"""

        errors = []
        for config in configurations:
            try:
                if getattr(current_context, 'id') == 1 and config[0] == 'role_id':
                    errors.append('You cannot change the role of the primary user admin.')
                    continue

                if config[0] == 'avatar_id' and config[0] in data:
                    image = self.get_existing_foreing_id(data, 'avatar_id', Media, session, True)
                    if not image or not Checker().is_image_type(image.type):
                        errors.append('The user avatar must be an image file.')
                        continue
                
                setattr(current_context, config[0], self.get_existing_foreing_id(data, config[0], config[1], session))

            except Exception as e:
                errors.append(str(e))
                
        return True if not errors else ErrorHandler().get_error(400, errors)


    def delegate_content_to_delete(self, user, session, request, context_list):
        """Delegates user's contents to superadmin (id=1) from list of context passed 
            by parameter context_list. Only do that if admin_new_owner is given as arg"""

        errors = []
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
                            errors.append('Could not find the super admin user.')
                else:
                    errors.append('You cannot delete this User because it has related ' + content_context.__tablename__ + '.')

        return True if not errors else  ErrorHandler().get_error(406, errors)