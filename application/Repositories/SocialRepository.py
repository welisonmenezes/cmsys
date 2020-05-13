from .RepositoryBase import RepositoryBase
from Models import Social, SocialSchema, Configuration, User
from Validators import SocialValidator
from Utils import Paginate, ErrorHandler, Checker, FilterBuilder

class SocialRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Social."""

    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def fn(session):
            fb = FilterBuilder(Social, args)
            fb.set_like_filter('name')
            fb.set_equals_filter('origin')
            fb.set_equals_filter('user_id')

            query = session.query(Social).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = SocialSchema(many=True)

            return {
                'data': schema.dump(result.items),
                'pagination': result.pagination
            }, 200

        return self.response(fn, False)
        

    def get_by_id(self, id):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def fn(session):
            result = session.query(Social).filter_by(id=id).first()
            schema = SocialSchema(many=False)

            return {
                'data': schema.dump(result)
            }, 200

        return self.response(fn, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def fn(session):
            data = request.get_json()

            if (data):
                validator = SocialValidator(data)

                if (validator.is_valid()):
                    social = Social(
                        name = data['name'],
                        url = data['url'],
                        target = data['target'],
                        description = data['description'],
                        origin = data['origin']
                    )

                    fk_was_added = self.add_foreign_keys(social, data, session)
                    if (fk_was_added != True):
                        return fk_was_added
                    
                    session.add(social)
                    session.commit()
                    last_id = social.id

                    return {
                        'message': 'Social saved successfully.',
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
                validator = SocialValidator(data)

                if (validator.is_valid(id=id)):
                    social = session.query(Social).filter_by(id=id).first()

                    if (social):
                        social.name = data['name']
                        social.url = data['url']
                        social.target = data['target']
                        social.origin = data['origin']
                        social.description = data['description']

                        fk_was_added = self.add_foreign_keys(social, data, session)
                        if (fk_was_added != True):
                            return fk_was_added

                        session.commit()

                        return {
                            'message': 'Social updated successfully.',
                            'id': social.id
                        }, 200
                    else:
                        return ErrorHandler().get_error(404, 'No Social found.')

                else:
                    return ErrorHandler().get_error(400, validator.get_errors())

            else:
                return ErrorHandler().get_error(400, 'No data send.')

        return self.response(fn, True)


    def delete(self, id):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def fn(session):
            social = session.query(Social).filter_by(id=id).first()

            if (social):
                session.delete(social)
                session.commit()

                return {
                    'message': 'Social deleted successfully.',
                    'id': id
                }, 200
            else:
                return ErrorHandler().get_error(404, 'No Social found.')

        return self.response(fn, True)

    
    def add_foreign_keys(self, social, data, session):
        """Controls if the configuration_id or user_id gets an existing foreign key data.
            Also checks if origin suitable to the foreign key requested."""
        
        try:
            if (social.origin == 'configuration'):
                if (not 'configuration_id' in data):
                    return ErrorHandler().get_error(400, 'If the origin field is configuration the field configuration_id is required')

                social.configuration_id = self.get_existing_foreing_id(data, 'configuration_id', Configuration, session)
                
            elif (social.origin == 'user'):
                if (not 'user_id' in data):
                    return ErrorHandler().get_error(400, 'If the origin field is user the field user_id is required')

                social.user_id = self.get_existing_foreing_id(data, 'user_id', User, session)

            return True

        except Exception as e:
            return ErrorHandler().get_error(400, e)