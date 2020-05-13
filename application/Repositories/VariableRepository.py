from .RepositoryBase import RepositoryBase
from Models import Variable, VariableSchema
from Validators import VariableValidator
from Utils import Paginate, ErrorHandler, Checker, FilterBuilder

class VariableRepository(RepositoryBase):
    """Works like a layer witch gets or transforms data and makes the
        communication between the controller and the model of Variable."""
    
    def get(self, args):
        """Returns a list of data recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            fb = FilterBuilder(Variable, args)

            try:
                fb.set_and_or_filter('s', 'or', [{'field':'key', 'type':'like'}, {'field':'value', 'type':'like'}])
            except Exception as e:
                return ErrorHandler().get_error(400, str(e))

            query = session.query(Variable).filter(*fb.get_filter()).order_by(*fb.get_order_by())
            result = Paginate(query, fb.get_page(), fb.get_limit())
            schema = VariableSchema(many=True)

            return {
                'data': schema.dump(result.items),
                'pagination': result.pagination
            }, 200

        return self.response(run, False)
        

    def get_by_id(self, id, args):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def run(session):
            schema = VariableSchema(many=False)
            result = session.query(Variable).filter_by(id=id).first()

            return {
                'data': schema.dump(result)
            }, 200

        return self.response(run, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def run(session):

            def process(session, data):
                variable = Variable(
                    key = data['key'],
                    value = data['value']
                )
                session.add(variable)
                session.commit()
                last_id = variable.id

                return {
                    'message': 'Variable saved successfully.',
                    'id': last_id
                }, 200

            return self.validate_before(process, request.get_json(), VariableValidator, session)

        return self.response(run, True)


    def update(self, id, request):
        """Updates the row whose id corresponding with the requested id.
            The data comes from the request object."""

        def run(session):

            def process(session, data):
                variable = session.query(Variable).filter_by(id=id).first()

                if (variable):
                    variable.key = data['key']
                    variable.value = data['value']
                    session.commit()

                    return {
                        'message': 'Variable updated successfully.',
                        'id': variable.id
                    }, 200
                else:
                    return ErrorHandler().get_error(404, 'No Variable found.')

            return self.validate_before(process, request.get_json(), VariableValidator, session, id=id)

        return self.response(run, True)


    def delete(self, id, request):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def run(session):
            variable = session.query(Variable).filter_by(id=id).first()

            if (variable):
                session.delete(variable)
                session.commit()

                return {
                    'message': 'Variable deleted successfully.',
                    'id': id
                }, 200
            else:
                return ErrorHandler().get_error(404, 'No Variable found.')

        return self.response(run, True)