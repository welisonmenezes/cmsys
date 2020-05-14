from .RepositoryBase import RepositoryBase
from Models import Capability, CapabilitySchema
from Validators import CapabilityValidator
from Utils import Paginate, ErrorHandler, FilterBuilder

class CapabilityRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Capability."""

    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(Capability, args)
            fb.set_equals_filter('type')
            fb.set_equals_filter('target_id')
            fb.set_equals_filter('can_write')
            fb.set_equals_filter('can_read')
            fb.set_equals_filter('can_delete')
            fb.set_like_filter('description')
            
            query = session.query(Capability).join(*self.joins).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = CapabilitySchema(many=True, exclude=self.get_exclude_fields(args, ['roles']))
            return self.handle_success(result, schema, 'get', 'Capability')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            schema = CapabilitySchema(many=False, exclude=self.get_exclude_fields(args, ['roles']))
            result = session.query(Capability).filter_by(id=id).first()
            return self.handle_success(result, schema, 'get_by_id', 'Capability')

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):

                identical_capability = self.verify_identical_capability(data, session)
                if identical_capability != False:
                    return ErrorHandler().get_error(400, 'The capability ' + str(identical_capability.id) + ' has exactly the same configurations.')

                capability = Capability(
                    description = data['description'],
                    type = data['type'],
                    target_id = data['target_id'],
                    can_write = data['can_write'],
                    can_read = data['can_read'],
                    can_delete = data['can_delete']
                )

                session.add(capability)
                session.commit()
                return self.handle_success(None, None, 'create', 'Capability', capability.id)

            return self.validate_before(process, request.get_json(), CapabilityValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):

                def fn(session, capability):

                    identical_capability = self.verify_identical_capability(data, session, id)
                    if identical_capability != False:
                        return ErrorHandler().get_error(400, 'The capability ' + str(identical_capability.id) + ' has exactly the same configurations.')

                    capability.description = data['description']
                    capability.type = data['type']
                    capability.target_id = data['target_id']
                    capability.can_write = data['can_write']
                    capability.can_read = data['can_read']
                    capability.can_delete = data['can_delete']
                    session.commit()
                    return self.handle_success(None, None, 'update', 'Capability', capability.id)
                
                return self.run_if_exists(fn, Capability, id, session)

            return self.validate_before(process, request.get_json(), CapabilityValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):

            def fn(session, capability):
                
                if (capability.roles):
                    return ErrorHandler().get_error(406, 'You cannot delete this Capability because it has a related Role.')

                session.delete(capability)
                session.commit()
                return self.handle_success(None, None, 'delete', 'Capability', id)

            return self.run_if_exists(fn, Capability, id, session)

        return self.response(run, True)