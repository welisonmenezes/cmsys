from .RepositoryBase import RepositoryBase
from Models import Role, RoleSchema, Capability
from Validators import RoleValidator, CapabilityValidator
from Utils import Paginate, ErrorHandler, Checker, FilterBuilder

class RoleRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Role."""

    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(Role, args)
            fb.set_equals_filter('can_access_admin')
            fb.set_like_filter('name')
            fb.set_like_filter('description')
            fb.set_equals_filter('capability_description', joined=Capability, joined_key='description')

            if (args['capability_description'] and args['capability_description'] != ''):
                self.joins.append(Role.capabilities)
            
            query = session.query(Role).join(*self.joins).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = RoleSchema(many=True, exclude=self.get_exclude_fields(args, ['capabilities']))

            return {
                'data': schema.dump(result.items),
                'pagination': result.pagination
            }, 200

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(Role).filter_by(id=id).first()
            schema = RoleSchema(many=False, exclude=self.get_exclude_fields(args, ['capabilities']))

            return {
                'data': schema.dump(result)
            }, 200

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):
                role = Role(
                    name = data['name'],
                    description = data['description'],
                    can_access_admin = data['can_access_admin'],
                )

                add_capabilite = self.add_capabilities(role, data, session)
                if (add_capabilite != True):
                    return add_capabilite

                session.add(role)
                session.commit()
                last_id = role.id

                return {
                    'message': 'Role saved successfully.',
                    'id': last_id
                }, 200

            return self.validate_before(process, request.get_json(), RoleValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):
                role = session.query(Role).filter_by(id=id).first()

                if (role):
                    role.name = data['name']
                    role.description = data['description']
                    role.can_access_admin = data['can_access_admin']

                    self.edit_capabilities(role, data, session)

                    add_capabilite = self.add_capabilities(role, data, session)
                    if (add_capabilite != True):
                        return add_capabilite

                    session.commit()

                    return {
                        'message': 'Role updated successfully.',
                        'id': role.id
                    }, 200
                else:
                    return ErrorHandler().get_error(404, 'No Role found.')

            return self.validate_before(process, request.get_json(), RoleValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):
            role = session.query(Role).filter_by(id=id).first()

            if (role):
                session.delete(role)
                session.commit()

                return {
                    'message': 'Role deleted successfully.',
                    'id': id
                }, 200
            else:
                return ErrorHandler().get_error(404, 'No Role found.')

        return self.response(run, True)


    def add_capabilities(self, role, data, session):
        """Adds capabilities, if it is possible, into the Role.
            First checks if capability with an id exists at data base, if so, includes it.
            If capability has no id, creates a new and then, include it."""

        if ('capabilities' in data and isinstance(data['capabilities'], list)):
            for capability in data['capabilities']:
                if ('id' in capability and Checker().can_be_integer(capability['id'])):
                    registered_capability = session.query(Capability).filter_by(id=int(capability['id'])).first()
                    if (registered_capability):
                        role.capabilities.append(registered_capability)
                    else:
                        return ErrorHandler().get_error(400, 'Capability ' + str(capability['id']) + ' does not exists.')
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
                        return ErrorHandler().get_error(400, capability_validator.get_errors())
        return True


    def edit_capabilities(self, role, data, session):
        """Edit the capabilities of the Role. It Checks between sended capabilities 
            and saved capabilities what must be deleted or added."""

        old_capabilities = []
        new_old_capabilities = []

        if (role.capabilities):
            for capability in role.capabilities:
                old_capabilities.append(capability.id)

        if ('capabilities' in data and isinstance(data['capabilities'], list)):
            for capability in data['capabilities']:
                if ('id' in capability and Checker().can_be_integer(capability['id'])):
                    new_old_capabilities.append(capability['id'])

        capabilities_to_delete = list(set(old_capabilities) - set(new_old_capabilities))

        for capability in capabilities_to_delete:
            registered_capability = session.query(Capability).filter_by(id=int(capability)).first()
            if (registered_capability):
                role.capabilities.remove(registered_capability)