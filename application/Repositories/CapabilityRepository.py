from .RepositoryBase import RepositoryBase
from Models import Capability, CapabilitySchema
from Validators import CapabilityValidator
from Utils import Paginate, FilterBuilder, Helper
from ErrorHandlers import BadRequestError

class CapabilityRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Capability."""

    def __init__(self, session):
        super().__init__(session)
        

    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(Capability, args)
            fb.set_equals_filters(['type', 'target_id', 'can_write', 'can_read', 'can_delete', 'only_themselves'])
            fb.set_like_filters(['description'])
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
                self.raise_if_has_identical_capability(data, session)
                capability = Capability()
                Helper().fill_object_from_data(capability, data, ['description', 'type', 'can_write', 'can_read', 'can_delete', 'only_themselves'])

                if 'target_id' in data:
                    capability.target_id = data['target_id']
                else:
                    capability.target_id = None

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
                    self.raise_if_has_identical_capability(data, session, id)
                    Helper().fill_object_from_data(capability, data, ['description', 'type', 'can_write', 'can_read', 'can_delete', 'only_themselves'])

                    if 'target_id' in data:
                        capability.target_id = data['target_id']
                    else:
                        capability.target_id = None
                        
                    session.commit()
                    return self.handle_success(None, None, 'update', 'Capability', capability.id)
                
                return self.run_if_exists(fn, Capability, id, session)

            return self.validate_before(process, request.get_json(), CapabilityValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):

            def fn(session, capability):
                if capability.roles:
                    raise BadRequestError('You cannot delete this Capability because it has a related Role.')
                session.delete(capability)
                session.commit()
                return self.handle_success(None, None, 'delete', 'Capability', id)

            return self.run_if_exists(fn, Capability, id, session)

        return self.response(run, True)


    def raise_if_has_identical_capability(self, data, session, id=None):	
        """Verifies if already exists another capability with exactly same values, if so, returns this."""	

        filter = (	
            Capability.type == data['type'],
            Capability.can_write == data['can_write'],	
            Capability.can_read == data['can_read'],	
            Capability.can_delete == data['can_delete'],
            Capability.only_themselves == data['only_themselves'],
        )

        if 'target_id' in data:	
            filter += (Capability.target_id == int(data['target_id']),)


        if id:	
            filter += (Capability.id != id,)	

        capability = session.query(Capability).filter(*filter).first()	

        if not capability:
            return capability
        else:
            raise BadRequestError('The capability ' + str(capability.id) + ' has exactly the same configurations.')