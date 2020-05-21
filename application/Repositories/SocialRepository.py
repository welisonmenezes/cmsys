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
                social = Social(
                    name = data['name'],
                    url = data['url'],
                    target = data['target'],
                    description = data['description'],
                    origin = data['origin']
                )

                fk_was_added = self.add_foreign_keys(social, data, session, [('configuration_id', Configuration), ('user_id', User)])
                if fk_was_added != True:
                    return fk_was_added
                
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
                    social.name = data['name']
                    social.url = data['url']
                    social.target = data['target']
                    social.origin = data['origin']
                    social.description = data['description']

                    fk_was_added = self.add_foreign_keys(social, data, session, [('configuration_id', Configuration), ('user_id', User)])
                    if fk_was_added != True:
                        return fk_was_added

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

        errors = []
        for config in configurations:
            try:
                setattr(current_context, config[0], None)

                if getattr(current_context, 'origin') == 'configuration' and config[0] == 'user_id' and 'user_id' in data:
                    errors.append('If the \'origin\' is \'configuration\' you dont have to send the \'user_id\'.')
                    continue

                if getattr(current_context, 'origin') == 'user' and config[0] == 'configuration_id' and 'configuration_id' in data:
                    errors.append('If the \'origin\' is \'user\' you dont have to send the \'configuration_id\'.')
                    continue
                
                setattr(current_context, config[0], self.get_existing_foreing_id(data, config[0], config[1], session))

            except Exception as e:
                errors.append(str(e))
                
        return True if not errors else ErrorHandler().get_error(400, errors)