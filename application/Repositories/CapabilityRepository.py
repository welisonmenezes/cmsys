from .RepositoryBase import RepositoryBase
from Models import Capability, CapabilitySchema
from Validators import CapabilityValidator
from Utils import Paginate, ErrorHandler, Checker, FilterBuilder

class CapabilityRepository(RepositoryBase):

    def set_query_fields(self, args):
        if (args['get_children'] and args['get_children'] == '1'):
            self.fields = [Capability]
        else:
            self.fields = [
                Capability.id,
                Capability.description,
                Capability.type,
                Capability.target_id, 
                Capability.can_write,
                Capability.can_read,
                Capability.can_delete
            ]

    
    def get(self, args):
        def fn(session):
            fb = FilterBuilder(Capability, args)
            fb.set_equals_filter('type')
            fb.set_equals_filter('target_id')
            fb.set_equals_filter('can_write')
            fb.set_equals_filter('can_read')
            fb.set_equals_filter('can_delete')
            fb.set_like_filter('description')
            filter = fb.get_filter()
            order_by = fb.get_order_by()
            page = fb.get_page()
            limit = fb.get_limit()

            self.set_query_fields(args)
            
            query = session.query(*self.fields).join(*self.joins).filter(*filter).order_by(*order_by)
            result = Paginate(query, page, limit)
            schema = CapabilitySchema(many=True)
            data = schema.dump(result.items)

            return {
                'data': data,
                'pagination': result.pagination
            }, 200

        return self.response(fn, False)
        

    def get_by_id(self, id, args):
        def fn(session):
            self.set_query_fields(args)

            schema = CapabilitySchema(many=False)
            result = session.query(*self.fields).filter_by(id=id).first()
            data = schema.dump(result)

            if (data):
                return {
                    'data': data
                }, 200
            else:
                return ErrorHandler(404, 'No Capability found.').response

        return self.response(fn, False)

    
    def create(self, request):
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
                    return ErrorHandler(400, validator.get_errors()).response

            else:
                return ErrorHandler(400, 'No data send.').response

        return self.response(fn, True)


    def update(self, id, request):
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
                        return ErrorHandler(404, 'No Capability found.').response

                else:
                    return ErrorHandler(400, validator.get_errors()).response

            else:
                return ErrorHandler(400, 'No data send.').response

        return self.response(fn, True)


    def delete(self, id):
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
                    return ErrorHandler(406, 'You cannot delete this Capability because it has related Role.').response

            else:
                return ErrorHandler(404, 'No Capability found.').response

        return self.response(fn, True)