from sqlalchemy import or_
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

        def fn(session):
            fb = FilterBuilder(Variable, args)
            filter = fb.get_filter()
            order_by = fb.get_order_by()
            page = fb.get_page()
            limit = fb.get_limit()

            if (args['s']):
                filter += (or_(Variable.key.like('%'+args['s']+'%'), Variable.value.like('%'+args['s']+'%')),)

            query = session.query(Variable).filter(*filter).order_by(*order_by)
            result = Paginate(query, page, limit)
            schema = VariableSchema(many=True)
            data = schema.dump(result.items)

            return {
                'data': data,
                'pagination': result.pagination
            }, 200

        return self.response(fn, False)
        

    def get_by_id(self, id):
        """Returns a single row found by id recovered from model.
            Before applies the received query params arguments."""

        def fn(session):
            schema = VariableSchema(many=False)
            result = session.query(Variable).filter_by(id=id).first()
            data = schema.dump(result)

            if (data):
                return {
                    'data': data
                }, 200
            else:
                return ErrorHandler().get_error(404, 'No Variable found.')

        return self.response(fn, False)

    
    def create(self, request):
        """Creates a new row based on the data received by the request object."""

        def fn(session):
            data = request.get_json()

            if (data):
                validator = VariableValidator(data)

                if (validator.is_valid()):
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
                validator = VariableValidator(data)

                if (validator.is_valid(id=id)):
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

                else:
                    return ErrorHandler().get_error(400, validator.get_errors())

            else:
                return ErrorHandler().get_error(400, 'No data send.')

        return self.response(fn, True)


    def delete(self, id):
        """Deletes, if it is possible, the row whose id corresponding with the requested id."""

        def fn(session):
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

        return self.response(fn, True)