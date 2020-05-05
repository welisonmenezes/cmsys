from sqlalchemy import or_
from Models import User, UserSchema, Media, Post, Role
from Validators import UserValidator
from Utils import Paginate, ErrorHandler, Checker, FilterBuilder
from .RepositoryBase import RepositoryBase

class UserRepository(RepositoryBase):
    
    def get(self, args):
        def fn(session):
            # filter params
            fb = FilterBuilder(User, args)
            fb.set_like_filter('email')
            fb.set_equals_filter('status')
            fb.set_equals_filter('role_id')

            if (args['get_role'] and args['get_role'] == '1'):
                fields = [User]
            else:
                fields = [User.id, User.login, User.password, User.first_name, User.last_name, User.email, User.registered, User.status, User.role_id, User.avatar_id, User.page_id]
            
            # TODO: implement get_avatar filter
            # TODO: implement get_page filter

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

            query = session.query(*fields).filter(*filter).order_by(*order_by)
            result = Paginate(query, page, limit)
            schema = UserSchema(many=True)
            data = schema.dump(result.items)

            return {
                'data': data,
                'pagination': result.pagination
            }, 200

        return self.response(fn, False)
        

    def get_by_id(self, id):
        def fn(session):
            schema = UserSchema(many=False)
            result = session.query(User).filter_by(id=id).first()
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
                    
                    # TODO: implement the following if block below as a single method

                    if ('role_id' in data):
                        role = session.query(Role.id).filter_by(id=int(data['role_id'])).first()
                        if (role):
                            user.role_id = role.id
                        else:
                            return ErrorHandler(400, 'Cannot Rind Role :' + str( data['role_id'])).response

                    if ('avatar_id' in data):
                        avatar = session.query(Media.id).filter_by(id=int(data['avatar_id'])).first()
                        if (avatar):
                            user.avatar_id = avatar.id
                        else:
                            return ErrorHandler(400, 'Cannot find Media :' + str( data['avatar_id'])).response

                    if ('page_id' in data):
                        post = session.query(Post.id).filter_by(id=int(data['page_id'])).first()
                        if (post):
                            user.page_id = post.id
                        else:
                            return ErrorHandler(400, 'Cannot find Post :' + str( data['page_id'])).response

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

                        if ('role_id' in data):
                            role = session.query(Role.id).filter_by(id=int(data['role_id'])).first()
                            if (role):
                                user.role_id = role.id
                            else:
                                return ErrorHandler(400, 'Cannot find Role :' + str( data['role_id'])).response

                        if ('avatar_id' in data):
                            avatar = session.query(Media.id).filter_by(id=int(data['avatar_id'])).first()
                            if (avatar):
                                user.avatar_id = avatar.id
                            else:
                                return ErrorHandler(400, 'Cannot find Media :' + str( data['avatar_id'])).response

                        if ('page_id' in data):
                            post = session.query(Post.id).filter_by(id=int(data['page_id'])).first()
                            if (post):
                                user.page_id = post.id
                            else:
                                return ErrorHandler(400, 'Cannot find Post :' + str( data['page_id'])).response

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
                # TODO: chekc if user has media (dont allow to delete)
                # TODO: check if user has social (delete social as well)
                # TODO: check if user has comments (delete comments as well)

                session.delete(user)
                session.commit()

                return {
                    'message': 'User deleted successfully.',
                    'id': id
                }, 200
            else:
                return ErrorHandler(404, 'No User found.').response

        return self.response(fn, True)