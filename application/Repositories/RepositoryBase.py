from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException
from Utils import ErrorHandler
from Models import Session

class RepositoryBase():
    """It Works like parent class witch must provide common attributes and methods
        and applies the response method to each child's method responder."""


    def __init__(self):
        """Starts the common attributes on instantiation of the class."""

        self.joins = []
        self.fields = []

    
    def response(self, run, need_rollback):
        """Applies the errors handling before returns a response.
            Must be implemented by methods of RepositoryBase's children classes."""

        session = Session()

        try:
            return run(session)

        except SQLAlchemyError as e:
            if (need_rollback):
                session.rollback()
            return ErrorHandler().get_error(500, str(e))

        except AttributeError as e:
            if (need_rollback):
                session.rollback()
            return ErrorHandler().get_error(400, str(e))

        except HTTPException as e:
            if (need_rollback):
                session.rollback()
            return ErrorHandler().get_error(500, str(e))
            
        finally:
            session.close()

    
    def validate_before(self, process, data, validator_context, session, id=None):
        """Validates the given data using the given validator before runs the given process."""

        if (data):
            validator = validator_context(data)

            if (validator.is_valid(id=id)):
                return process(session, data)

            else:
                return ErrorHandler().get_error(400, validator.get_errors())

        else:
            return ErrorHandler().get_error(400, 'No data send.')

    
    def get_existing_foreing_id(self, data, key, context, session, get_all_filelds= False):
        """Checks if a given id exists as primary key of the given context (a model) and returns it.
            Also is possible returns the complete row if get_all_fields is true."""

        if (key in data):
            if (get_all_filelds):
                element = session.query(context).filter_by(id=int(data[key])).first()
            else:
                element = session.query(getattr(context, 'id')).filter_by(id=int(data[key])).first()
                
            if (element):
                return element if get_all_filelds else element.id
            else:
                raise Exception('Cannont find '+ str(context.__tablename__) + ': ' + str( data[key]))

    
    def get_exclude_fields(self, args, fields):
        """Returns the fields witch must be ignored by the sql query.
            The arguments received by parameters determines the correct behave."""

        exclude_fields = ()

        if fields and isinstance(fields, list):
            for field in fields:
                if (not args['get_' + str(field)] or args['get_' + str(field)] != '1'):
                    exclude_fields += (field,)

        return exclude_fields


    def handle_success(self, result, schema, type, model_name='', id=None):
        """Handles almost all possible success returns."""

        if type == 'get':
            return { 'data': schema.dump(result.items), 'pagination': result.pagination }, 200
        elif type == 'get_by_id':
            return { 'data': schema.dump(result) }, 200
        elif type == 'create':
            return { 'message': model_name + ' saved successfully.', 'id': id }, 200
        elif type == 'update':
            return { 'message': model_name + ' updated successfully.', 'id': id }, 200
        elif type == 'delete':
            return { 'message': model_name + ' deleted successfully.', 'id': id }, 200
        else:
            return ErrorHandler().get_error(500, 'Invalid success error handler parameters.')