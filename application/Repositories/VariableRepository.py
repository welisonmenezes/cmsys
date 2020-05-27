from .RepositoryBase import RepositoryBase
from Models import Variable, VariableSchema
from Validators import VariableValidator
from Utils import Paginate, FilterBuilder, Helper
from ErrorHandlers import BadRequestError

class VariableRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Variable."""

    def __init__(self, session):
        super().__init__(session)
        
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(Variable, args)

            try:
                fb.set_and_or_filter('s', 'or', [{'field':'key', 'type':'like'}, {'field':'value', 'type':'like'}])
            except Exception as e:
                raise BadRequestError(str(e))

            query = session.query(Variable).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = VariableSchema(many=True)
            return self.handle_success(result, schema, 'get', 'Variable')

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            schema = VariableSchema(many=False)
            result = session.query(Variable).filter_by(id=id).first()
            return self.handle_success(result, schema, 'get_by_id', 'Variable')

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):
                variable = Variable()
                Helper().fill_object_from_data(variable, data, ['key', 'value'])
                session.add(variable)
                session.commit()
                return self.handle_success(None, None, 'create', 'Variable', variable.id)

            return self.validate_before(process, request.get_json(), VariableValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):

                def fn(session, variable):
                    Helper().fill_object_from_data(variable, data, ['key', 'value'])
                    session.commit()
                    return self.handle_success(None, None, 'update', 'Variable', variable.id)

                return self.run_if_exists(fn, Variable, id, session)

            return self.validate_before(process, request.get_json(), VariableValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):

            def fn(session, variable):
                session.delete(variable)
                session.commit()
                return self.handle_success(None, None, 'delete', 'Variable', id)
            
            return self.run_if_exists(fn, Variable, id, session)

        return self.response(run, True)