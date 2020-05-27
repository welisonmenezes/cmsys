from .RepositoryBase import RepositoryBase
from Models import Configuration, ConfigurationSchema, Language
from Validators import ConfigurationValidator
from Utils import Paginate, FilterBuilder, Helper
from ErrorHandlers import BadRequestError

# TODO: from configuration to be able to save/update/delete socials

class ConfigurationRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Configuration."""

    def __init__(self, session):
        super().__init__(session)
        
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(Configuration, args)
            fb.set_equals_filters(['language_id'])

            try:
                fb.set_and_or_filter('s', 'or', [{'field':'title', 'type':'like'}, {'field':'description', 'type':'like'}])
            except Exception as e:
                raise BadRequestError(str(e))

            query = session.query(Configuration).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = ConfigurationSchema(many=True, exclude=self.get_exclude_fields(args, ['language', 'socials']))
            return self.handle_success(result, schema, 'get', 'Configuration')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(Configuration).filter_by(id=id).first()
            schema = ConfigurationSchema(many=False, exclude=self.get_exclude_fields(args, ['language', 'socials']))
            return self.handle_success(result, schema, 'get_by_id', 'Configuration')

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):
                configuration = Configuration()
                Helper().fill_object_from_data(configuration, data, ['title', 'description', 'has_comments', 'email'])
                self.add_foreign_keys(configuration, data, session, [('language_id', Language)])
                session.add(configuration)
                session.commit()
                return self.handle_success(None, None, 'create', 'Configuration', configuration.id)

            return self.validate_before(process, request.get_json(), ConfigurationValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):

                def fn(session, configuration):
                    Helper().fill_object_from_data(configuration, data, ['title', 'description', 'has_comments', 'email'])
                    self.add_foreign_keys(configuration, data, session, [('language_id', Language)])
                    session.commit()
                    return self.handle_success(None, None, 'update', 'Configuration', configuration.id)
                
                return self.run_if_exists(fn, Configuration, id, session)

            return self.validate_before(process, request.get_json(), ConfigurationValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):

            if id == 1:
                raise BadRequestError('The Primary configuration row cannot be deleted.')

            def fn(session, configuration):
                session.delete(configuration)
                session.commit()
                return self.handle_success(None, None, 'delete', 'Configuration', id)

            return self.run_if_exists(fn, Configuration, id, session)

        return self.response(run, True)