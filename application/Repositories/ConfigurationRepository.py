from .RepositoryBase import RepositoryBase
from Models import Configuration, ConfigurationSchema
from Validators import ConfigurationValidator
from Utils import Paginate, ErrorHandler, FilterBuilder

class ConfigurationRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Configuration."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(Configuration, args)
            # fb.set_equals_filter('type')
            # fb.set_equals_filter('target')
            # fb.set_like_filter('value')

            query = session.query(Configuration).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = ConfigurationSchema(many=True)
            return self.handle_success(result, schema, 'get', 'Configuration')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            result = session.query(Configuration).filter_by(id=id).first()
            schema = ConfigurationSchema(many=False)
            return self.handle_success(result, schema, 'get_by_id', 'Configuration')

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):

                configuration = Configuration(
                    title = data['title'],
                    description = data['description'],
                    has_comments = data['has_comments'],
                    email = data['email'],
                    language_id = data['language_id']
                )
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
                configuration = session.query(Configuration).filter_by(id=id).first()

                if (configuration):
                    configuration.title = data['title']
                    configuration.description = data['description']
                    configuration.has_comments = data['has_comments']
                    configuration.email = data['email']
                    configuration.language_id = data['language_id']
                    session.commit()
                    return self.handle_success(None, None, 'update', 'Configuration', configuration.id)

                else:
                    return ErrorHandler().get_error(404, 'No Configuration found.')

            return self.validate_before(process, request.get_json(), ConfigurationValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):
            configuration = session.query(Configuration).filter_by(id=id).first()

            if (configuration):
                session.delete(configuration)
                session.commit()
                return self.handle_success(None, None, 'delete', 'Configuration', id)

            else:
                return ErrorHandler().get_error(404, 'No Configuration found.')

        return self.response(run, True)