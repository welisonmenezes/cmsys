from .RepositoryBase import RepositoryBase
from Models import Social, SocialSchema, Configuration, User
from Validators import SocialValidator
from Utils import Paginate, FilterBuilder, Helper
from ErrorHandlers import BadRequestError

class SocialRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Social."""

    def __init__(self, session):
        super().__init__(session)
        

    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(Social, args)
            fb.set_like_filters(['name'])
            fb.set_equals_filters(['origin', 'user_id'])
            query = session.query(Social).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = SocialSchema(many=True, exclude=self.get_exclude_fields(args, ['user', 'configuration']))
            return self.handle_success(result, schema, 'get', 'Social')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(Social).filter_by(id=id).first()
            schema = SocialSchema(many=False, exclude=self.get_exclude_fields(args, ['user', 'configuration']))
            return self.handle_success(result, schema, 'get_by_id', 'Social')

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):
                social = Social()
                Helper().fill_object_from_data(social, data, ['name', 'url', 'target', 'description', 'origin'])
                self.add_foreign_keys(social, data, session, [('configuration_id', Configuration), ('user_id', User)])
                session.add(social)
                session.commit()
                return self.handle_success(None, None, 'create', 'Social', social.id)

            return self.validate_before(process, request.get_json(), SocialValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):

                def fn(session, social):
                    Helper().fill_object_from_data(social, data, ['name', 'url', 'target', 'description', 'origin'])
                    self.add_foreign_keys(social, data, session, [('configuration_id', Configuration), ('user_id', User)])
                    session.commit()
                    return self.handle_success(None, None, 'update', 'Social', social.id)

                return self.run_if_exists(fn, Social, id, session)

            return self.validate_before(process, request.get_json(), SocialValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):

            def fn(session, social):
                session.delete(social)
                session.commit()
                return self.handle_success(None, None, 'delete', 'Social', id)

            return self.run_if_exists(fn, Social, id, session)

        return self.response(run, True)


    def add_foreign_keys(self, current_context, data, session, configurations):
        """Controls if the list of foreign keys is an existing foreign key data. How to use:
            The configurtations must like: [('foreign_key_at_target_context, target_context)]"""

        for config in configurations:
            try:
                setattr(current_context, config[0], None)

                if getattr(current_context, 'origin') == 'configuration' and config[0] == 'user_id' and 'user_id' in data:
                    raise BadRequestError('If the \'origin\' is \'configuration\' you dont have to send the \'user_id\'.')

                if getattr(current_context, 'origin') == 'user' and config[0] == 'configuration_id' and 'configuration_id' in data:
                    raise BadRequestError('If the \'origin\' is \'user\' you dont have to send the \'configuration_id\'.')
                
                setattr(current_context, config[0], self.get_existing_foreing_id(data, config[0], config[1], session))

            except Exception as e:
                raise BadRequestError(str(e))