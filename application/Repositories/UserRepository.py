from sqlalchemy import or_
from .RepositoryBase import RepositoryBase
from Models import User, UserSchema, Media, Post, Role, Social
from Validators import UserValidator
from Utils import Paginate, ErrorHandler, Checker, FilterBuilder
from flask import  request


class UserRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of User."""

    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def fn(session):
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
            order_by = fb.get_order_by()
            page = fb.get_page()
            limit = fb.get_limit()

            if (args['name']):
                filter += (or_(User.first_name.like('%'+args['name']+'%'), User.last_name.like('%'+args['name']+'%'), User.nickname.like('%'+args['name']+'%')),)

            query = session.query(User).filter(*filter).order_by(*order_by)
            result = Paginate(query, page, limit)
            schema = UserSchema(many=True, exclude=self.get_exclude_fields(args, ['role', 'socials']))
            data = schema.dump(result.items)

            return {
                'data': data,
                'pagination': result.pagination
            }, 200

        return self.response(fn, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def fn(session):
            schema = UserSchema(many=False, exclude=self.get_exclude_fields(args, ['role', 'socials']))
            result = session.query(User).filter_by(id=id).first()
            data = schema.dump(result)

            if (data):
                return {
                    'data': data
                }, 200
            else:
                return ErrorHandler().get_error(404, 'No User found.')

        return self.response(fn, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def fn(session):
            data = request.get_json()

            # TODO: implement password cryptography

            if (data):
                validator = UserValidator(data)

                if (validator.is_valid()):
                    user = User(
                        login = data['login'],
                        password = data['password'],
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
                else:
                    return ErrorHandler().get_error(400, validator.get_errors())

            else:
                return ErrorHandler().get_error(400, 'No data send.')

        return self.response(fn, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def fn(session):
            data = request.get_json()

            if (data):
                validator = UserValidator(data)

                if (validator.is_valid(id=id)):
                    user = session.query(User).filter_by(id=id).first()

                    if (user):
                        user.login = data['login']
                        user.password = data['password']
                        user.nickname = data['nickname']
                        user.first_name = data['first_name']
                        user.last_name = data['last_name']
                        user.email = data['email']
                        user.status = data['status']

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

                else:
                    return ErrorHandler().get_error(400, validator.get_errors())

            else:
                return ErrorHandler().get_error(400, 'No data send.')

        return self.response(fn, True)


    def delete(self, id):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def fn(session):
            user = session.query(User).filter_by(id=id).first()

            if user:
                
                # TODO: check if user has post (dont allow to delete)
                # TODO: check if user has comments (delete comments as well)
                # TODO: don't allow to delete user with id 1

                # delete or delegate user medias
                image_was_deleted = self.delete_or_delegate_user_media(user, session)
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

        return self.response(fn, True)


    def add_foreign_keys(self, user, data, session):
        """Controls if the role_id, page_id and avatar_id an existing foreign key data.
            Also checks if the avatar_id refers to an image file type."""

        try:
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

    
    def delete_or_delegate_user_media(self, user, session):
        """Deletes user's medias or delegates they to user superadmin (id=1)"""

        media = session.query(Media.id).filter_by(user_id=user.id).first()
        if media:
            if 'admin_new_owner' in request.args and request.args['admin_new_owner'] == '1':
                medias = session.query(Media).filter_by(user_id=user.id).all()
                for m in medias:
                    admin = session.query(User).filter_by(id=1).first()
                    if admin:
                        m.user_id = admin.id
                    else:
                        return ErrorHandler().get_error(406, 'Could not find the super admin user.') 
            else:
                return ErrorHandler().get_error(406, 'You cannot delete this User because it has related Media.')
        
        return True