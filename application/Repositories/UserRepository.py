from sqlalchemy import or_
from app import bcrypt
from .RepositoryBase import RepositoryBase
from Models import User, UserSchema, Media, Post, Role, Social
from Validators import UserValidator
from Utils import Paginate, ErrorHandler, Checker, FilterBuilder


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
            except Exception as e:
                return ErrorHandler().get_error(400, str(e))

            filter = fb.get_filter()
            if (args['name']):
                filter += (or_(User.first_name.like('%'+args['name']+'%'), User.last_name.like('%'+args['name']+'%'), User.nickname.like('%'+args['name']+'%')),)

            query = session.query(User).filter(*filter).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            excluded_fields = self.get_exclude_fields(args, ['role', 'socials'])
            excluded_fields += ('password',)
            schema = UserSchema(many=True, exclude=excluded_fields)

            return {
                'data': schema.dump(result.items),
                'pagination': result.pagination
            }, 200

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(User).filter_by(id=id).first()
            excluded_fields = self.get_exclude_fields(args, ['role', 'socials'])
            excluded_fields += ('password',)
            schema = UserSchema(many=False, exclude=excluded_fields)

            return {
                'data': schema.dump(result)
            }, 200

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
                    status = data['status']
                )
                
                fk_was_added = self.add_foreign_keys(user, data, session)
                if (fk_was_added != True):
                    return fk_was_added

                session.add(user)
                session.commit()
                last_id = user.id

                return {
                    'message': 'User saved successfully.',
                    'id': last_id
                }, 200

            return self.validate_before(process, request.get_json(), UserValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):
                user = session.query(User).filter_by(id=id).first()

                if (user):
                    user.login = data['login']
                    user.nickname = data['nickname']
                    user.first_name = data['first_name']
                    user.last_name = data['last_name']
                    user.email = data['email']
                    user.status = data['status']

                    if data['password'] != '' and not bcrypt.check_password_hash(user.password, data['password']):
                        user.password = bcrypt.generate_password_hash(data['password'])

                    fk_was_added = self.add_foreign_keys(user, data, session)
                    if (fk_was_added != True):
                        return fk_was_added

                    session.commit()

                    return {
                        'message': 'User updated successfully.',
                        'id': user.id
                    }, 200
                else:
                    return ErrorHandler().get_error(404, 'No User found.')

            return self.validate_before(process, request.get_json(), UserValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        if id == 1:
            return ErrorHandler().get_error(400, 'The Super Admin user cannot be deleted.')

        def run(session):
            
            user = session.query(User).filter_by(id=id).first()

            if user:
                
                # TODO: check if user has post (dont allow to delete or delegato to superadmin)
                # TODO: check if user has comments (delete comments as well)

                # delete or delegate user medias
                image_was_deleted = self.delete_or_delegate_user_contents(user,session, Media, request)
                if image_was_deleted != True:
                    return image_was_deleted

                # delete user socials
                session.query(Social).filter_by(user_id=user.id).delete(synchronize_session='evaluate')

                session.delete(user)
                session.commit()

                return {
                    'message': 'User deleted successfully.',
                    'id': id
                }, 200
            else:
                return ErrorHandler().get_error(404, 'No User found.')

        return self.response(run, True)


    def add_foreign_keys(self, user, data, session):
        """Controls if the role_id, page_id and avatar_id are an existing foreign key data.
            Also checks if the avatar_id refers to an image file type."""

        try:
            if (user.id != 1): # Cannot change Super Admin user role.
                user.role_id = self.get_existing_foreing_id(data, 'role_id', Role, session)

            user.page_id = self.get_existing_foreing_id(data, 'page_id', Post, session)

            image = self.get_existing_foreing_id(data, 'avatar_id', Media, session, True)
            if image:
                if Checker().is_image_type(image.type):
                    user.avatar_id = image.id
                else:
                    return ErrorHandler().get_error(400, 'The user avatar must be an image file.')

            return True

        except Exception as e:
            return ErrorHandler().get_error(400, e)


    def delete_or_delegate_user_contents(self, user, session, content_context, request):
        """Deletes user's contents from content_context passed by parameter
            or delegates they to user superadmin (id=1)"""

        content = session.query(content_context).filter_by(user_id=user.id).first()
        if content:
            if 'admin_new_owner' in request.args and request.args['admin_new_owner'] == '1':
                contents = session.query(content_context).filter_by(user_id=user.id).all()
                for c in contents:
                    admin = session.query(User).filter_by(id=1).first()
                    if admin:
                        c.user_id = admin.id
                    else:
                        return ErrorHandler().get_error(406, 'Could not find the super admin user.') 
            else:
                return ErrorHandler().get_error(406, 'You cannot delete this User because it has related xxxx.')
        
        return True