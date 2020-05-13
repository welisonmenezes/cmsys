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

        def fn(session):
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

            return {
                'data': schema.dump(result.items),
                'pagination': result.pagination
            }, 200

        return self.response(fn, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def fn(session):
            schema = CapabilitySchema(many=False, exclude=self.get_exclude_fields(args, ['roles']))
            result = session.query(Capability).filter_by(id=id).first()

            return {
                'data': schema.dump(result)
            }, 200

        return self.response(fn, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def fn(session):
            data = request.get_json()

            if (data):
                validator = CapabilityValidator(data)

                if (validator.is_valid()):
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
                    last_id = capability.id

                    return {
                        'message': 'Capability saved successfully.',
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
                validator = CapabilityValidator(data)

                if (validator.is_valid(id=id)):
                    capability = session.query(Capability).filter_by(id=id).first()

                    if (capability):
                        capability.description = data['description']
                        capability.type = data['type']
                        capability.target_id = data['target_id']
                        capability.can_write = data['can_write']
                        capability.can_read = data['can_read']
                        capability.can_delete = data['can_delete']
                        session.commit()

                        return {
                            'message': 'Capability updated successfully.',
                            'id': capability.id
                        }, 200
                    else:
                        return ErrorHandler().get_error(404, 'No Capability found.')

                else:
                    return ErrorHandler().get_error(400, validator.get_errors())

            else:
                return ErrorHandler().get_error(400, 'No data send.')

        return self.response(fn, True)


    def delete(self, id):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def fn(session):
            capability = session.query(Capability).filter_by(id=id).first()

            if (capability):

                if (not capability.roles):
                    session.delete(capability)
                    session.commit()

                    return {
                        'message': 'Capability deleted successfully.',
                        'id': id
                    }, 200

                else:
                    return ErrorHandler().get_error(406, 'You cannot delete this Capability because it has related Role.')

            else:
                return ErrorHandler().get_error(404, 'No Capability found.')

        return self.response(fn, True)