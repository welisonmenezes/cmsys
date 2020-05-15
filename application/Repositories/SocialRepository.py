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
            fb.set_like_filter('name')
            fb.set_equals_filter('origin')
            fb.set_equals_filter('user_id')

            query = session.query(Social).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = SocialSchema(many=True)
            return self.handle_success(result, schema, 'get', 'Social')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(Social).filter_by(id=id).first()
            schema = SocialSchema(many=False)
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