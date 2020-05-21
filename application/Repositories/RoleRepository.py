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
            fb.set_equals_filters(['can_access_admin'])
            fb.set_like_filters(['name', 'description'])

            fb.set_like_filter('capability_description', joined=Capability, joined_key='description')
            if (args['capability_description'] and args['capability_description'] != ''):
                self.joins.append(Role.capabilities)
            
            query = session.query(Role).join(*self.joins).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = RoleSchema(many=True, exclude=self.get_exclude_fields(args, ['capabilities']))
            return self.handle_success(result, schema, 'get', 'Role')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(Role).filter_by(id=id).first()
            schema = RoleSchema(many=False, exclude=self.get_exclude_fields(args, ['capabilities']))
            return self.handle_success(result, schema, 'get_by_id', 'Role')

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
                self.add_many_to_many_relationship('capabilities', role, data, Capability, session)
                session.add(role)
                session.commit()
                return self.handle_success(None, None, 'create', 'Role', role.id)

            return self.validate_before(process, request.get_json(), RoleValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):

                def fn(session, role):
                    role.name = data['name']
                    role.description = data['description']
                    role.can_access_admin = data['can_access_admin']
                    self.edit_capabilities(role, data, session)
                    self.edit_many_to_many_relationship('capabilities', role, data, Capability, session)
                    session.commit()
                    return self.handle_success(None, None, 'update', 'Role', role.id)

                return self.run_if_exists(fn, Role, id, session)

                role = session.query(Role).filter_by(id=id).first()

            return self.validate_before(process, request.get_json(), RoleValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):

            def fn(session, role):
                session.delete(role)
                session.commit()
                return self.handle_success(None, None, 'delete', 'Role', id)

            return self.run_if_exists(fn, Role, id, session)

        return self.response(run, True)