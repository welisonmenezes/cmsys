from sqlalchemy import or_
from .RepositoryBase import RepositoryBase
from Models import User, UserSchema, Media, Post, Role
from Validators import UserValidator
from Utils import Paginate, ErrorHandler, Checker, FilterBuilder

class UserRepository(RepositoryBase):

    def set_query_fields(self, args):
        if (args['get_children'] and args['get_children'] == '1'):
            self.fields = [User]
        else:
            self.fields = [
                User.id,
                User.login,
                User.password,
                User.first_name,
                User.last_name,
                User.email,
                User.registered,
                User.status,
                User.role_id,
                User.avatar_id,
                User.page_id
            ]


    def get(self, args):
        def fn(session):
            fb = FilterBuilder(User, args)
            fb.set_like_filter('email')
            fb.set_equals_filter('status')
            fb.set_equals_filter('role_id')

            self.set_query_fields(args)

            try:
                fb.set_date_filter('registered', date_modifier=args['date_modifier'])
            except Exception as e:
                return ErrorHandler(400, e).response

            filter = fb.get_filter()
            order_by = fb.get_order_by()
            page = fb.get_page()
            limit = fb.get_limit()

            if (args['name']):
                filter += (or_(User.first_name.like('%'+args['name']+'%'), User.last_name.like('%'+args['name']+'%'), User.nickname.like('%'+args['name']+'%')),)

            query = session.query(*self.fields).filter(*filter).order_by(*order_by)
            result = Paginate(query, page, limit)
            schema = UserSchema(many=True)
            data = schema.dump(result.items)

            return {
                'data': data,
                'pagination': result.pagination
            }, 200

        return self.response(fn, False)
        

    def get_by_id(self, id, args):
        def fn(session):

            self.set_query_fields(args)

            schema = UserSchema(many=False)
            result = session.query(*self.fields).filter_by(id=id).first()
            data = schema.dump(result)

            if (data):
                return {
                    'data': data
                }, 200
            else:
                return ErrorHandler(404, 'No User found.').response

        return self.response(fn, False)

    
    def create(self, request):
        def fn(session):
            data = request.get_json()

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
                    
                    # add forgein elements
                    try:
                        user.role_id = self.get_existing_foreing_id(data, 'role_id', Role, session)
                        user.avatar_id = self.get_existing_foreing_id(data, 'avatar_id', Media, session)
                        user.page_id = self.get_existing_foreing_id(data, 'page_id', Post, session)
                    except Exception as e:
                        return ErrorHandler(400, e).response

                    session.add(user)
                    session.commit()
                    last_id = user.id

                    return {
                        'message': 'User saved successfully.',
                        'id': last_id
                    }, 200
                else:
                    return ErrorHandler(400, validator.get_errors()).response

            else:
                return ErrorHandler(400, 'No data send.').response

        return self.response(fn, True)


    def update(self, id, request):
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

                        # add forgein elements
                        try:
                            user.role_id = self.get_existing_foreing_id(data, 'role_id', Role, session)
                            user.avatar_id = self.get_existing_foreing_id(data, 'avatar_id', Media, session)
                            user.page_id = self.get_existing_foreing_id(data, 'page_id', Post, session)
                        except Exception as e:
                            return ErrorHandler(400, e).response

                        session.commit()

                        return {
                            'message': 'User updated successfully.',
                            'id': user.id
                        }, 200
                    else:
                        return ErrorHandler(404, 'No User found.').response

                else:
                    return ErrorHandler(400, validator.get_errors()).response

            else:
                return ErrorHandler(400, 'No data send.').response

        return self.response(fn, True)


    def delete(self, id):
        def fn(session):
            user = session.query(User).filter_by(id=id).first()

            if (user):

                # TODO: check if user has post (dont allow to delete)
                # TODO: enable to delete user by parameter 'admin_new_owner' to delegate to admin his medias
                # TODO: check if user has social (delete social as well)
                # TODO: check if user has comments (delete comments as well)

                media = session.query(Media.id).filter_by(user_id=user.id).first()
                if (media):
                    return ErrorHandler(406, 'You cannot delete this User because it has related Media.').response

                session.delete(user)
                session.commit()

                return {
                    'message': 'User deleted successfully.',
                    'id': id
                }, 200
            else:
                return ErrorHandler(404, 'No User found.').response

        return self.response(fn, True)