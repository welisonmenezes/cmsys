from Models import Role, RoleSchema, Capability
from Validators import RoleValidator, CapabilityValidator
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

            if (args['get_capabilities'] and args['get_capabilities'] == '1'):
                query = session.query(Role).filter(*filter)
            else:
                query = session.query(
                    Role.id, Role.name,
                    Role.description,
                    Role.can_access_admin
                ).filter(*filter)

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
                        can_access_admin = data['can_access_admin'],
                    )

                    add_capabilite = self.add_capability(role, data, session)
                    if (add_capabilite != True):
                        return add_capabilite

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


    def add_capability(self, role, data, session):
        if ('capabilities' in data and isinstance(data['capabilities'], list)):
            for capability in data['capabilities']:
                if ('id' in capability and Checker.can_be_integer(capability['id'])):
                    registered_capability = session.query(Capability).filter_by(id=int(capability['id'])).first()
                    if (registered_capability):
                        role.capabilities.append(registered_capability)
                    else:
                        return ErrorHandler(400, 'Capability ' + str(capability['id']) + ' does not exists.').response
                else:
                    capability_validator = CapabilityValidator(capability)
                    if (capability_validator.is_valid()):
                        capability = Capability(
                            description = capability['description'],
                            type = capability['type'],
                            target_id = capability['target_id'],
                            can_write = capability['can_write'],
                            can_read = capability['can_read'],
                            can_delete = capability['can_delete']
                        )
                        role.capabilities.append(capability)
                    else:
                        capability_validator.get_errors().insert(0, {
                            'message': 'Check if all Capability object is configured correctly.'
                        })
                        return ErrorHandler(400, capability_validator.get_errors()).response
        return True