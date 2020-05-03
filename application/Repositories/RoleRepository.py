from Models import Role, RoleSchema
from Validators import RoleValidator
from Utils import Paginate, ErrorHandler, Checker
from .RepositoryBase import RepositoryBase

class RoleRepository(RepositoryBase):
    
    def get(self, args):
        def fn(session):
            filter = ()
            page = 1
            limit = 10

            if (args['page'] and Checker.can_be_integer(args['page'])):
                page = int(args['page'])

            if (args['limit'] and Checker.can_be_integer(args['limit'])):
                limit = int(args['limit'])

            if (args['name']):
                filter += (Role.name.like('%' + args['name'] + '%'),)

            if (args['description']):
                filter += (Role.description.like('%' + args['description'] + '%'),)

            if (args['can_access_admin']):
                filter += (Role.can_access_admin == args['can_access_admin'],)

            schema = RoleSchema(many=True)
            query = session.query(Role).filter(*filter)
            result = Paginate(query, page, limit)
            data = schema.dump(result.items)

            return {
                'data': data,
                'pagination': result.pagination
            }, 200

        return self.response(fn, False)
        

    def get_by_id(self, id):
        def fn(session):
            schema = RoleSchema(many=False)
            result = session.query(Role).filter_by(id=id).first()
            data = schema.dump(result)

            if (data):
                return {
                    'data': data
                }, 200
            else:
                return ErrorHandler(404, 'No Role found.').response

        return self.response(fn, False)

    
    def create(self, request):
        def fn(session):
            data = request.get_json()

            if (data):
                validator = RoleValidator(data)

                if (validator.is_valid()):
                    role = Role(
                        name = data['name'],
                        description = data['description'],
                        can_access_admin = data['can_access_admin']
                    )
                    session.add(role)
                    session.commit()
                    last_id = role.id

                    return {
                        'message': 'Role saved successfully.',
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
                validator = RoleValidator(data)

                if (validator.is_valid()):
                    role = session.query(Role).filter_by(id=id).first()

                    if (role):
                        role.name = data['name']
                        role.description = data['description']
                        role.can_access_admin = data['can_access_admin']
                        session.commit()

                        return {
                            'message': 'Role updated successfully.',
                            'id': role.id
                        }, 200
                    else:
                        return ErrorHandler(404, 'No Role found.').response

                else:
                    return ErrorHandler(400, validator.get_errors()).response

            else:
                return ErrorHandler(400, 'No data send.').response

        return self.response(fn, True)


    def delete(self, id):
        def fn(session):
            role = session.query(Role).filter_by(id=id).first()

            if (role):
                session.delete(role)
                session.commit()

                return {
                    'message': 'Role deleted successfully.',
                    'id': id
                }, 200
            else:
                return ErrorHandler(404, 'No Role found.').response

        return self.response(fn, True)