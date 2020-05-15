from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException
from Utils import ErrorHandler, Checker
from Models import Session, Media

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


    def run_if_exists(self, fn, context, id, session):
        """Runs the given method if the given element exists at the database."""

        element = session.query(context).filter_by(id=id).first()
        if (element):
            return fn(session, element)
        else:
            return ErrorHandler().get_error(404, 'No ' + context.__tablename__ + ' found.')


    def get_result_by_unique_key(self, id, context, session):
        if Checker().can_be_integer(id):
            return session.query(context).filter_by(id=id).first()
        else:
            return session.query(context).filter_by(name=id).first()

    
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


    def is_foreigners(self, configurations, session):
        """Verifies if is a foreigner on any given context at configuration, if so, return errors. How to use:
            The configuration must like: [(current_context, foreign_key_at_target_context, target_context)]"""

        errors = []
        for config in configurations:
            filter = (getattr(config[2], config[1])==getattr(config[0], 'id'),)
            element = session.query(getattr(config[2], 'id')).filter(*filter).first()
            if (element):
                errors.append('You cannot delete this ' + config[0].__class__.__name__ + ' because it has a related ' + config[2].__tablename__)

        return False if not errors else ErrorHandler().get_error(406, errors)


    def add_foreign_keys(self, current_context, data, session, configurations):
        """Controls if the list of foreign keys is an existing foreign key data. How to use:
            The configurtations must like: [('foreign_key_at_target_context, target_context)]"""

        errors = []
        for config in configurations:
            try:
                if current_context.__tablename__ == 'Social':
                    setattr(current_context, config[0], None)

                    if getattr(current_context, 'origin') == 'configuration' and config[0] == 'user_id' or \
                        getattr(current_context, 'origin') == 'user' and config[0] == 'configuration_id':
                        continue

                if current_context.__tablename__ == 'User':
                    if getattr(current_context, 'id') == 1 and config[0] == 'role_id':
                        continue

                    if config[0] == 'avatar_id' and config[0] in data:
                        image = self.get_existing_foreing_id(data, 'avatar_id', Media, session, True)
                        if not image or not Checker().is_image_type(image.type):
                            return ErrorHandler().get_error(400, 'The user avatar must be an image file.')

                setattr(current_context, config[0], self.get_existing_foreing_id(data, config[0], config[1], session))

            except Exception as e:
                errors.append(str(e))
                
        return True if not errors else ErrorHandler().get_error(400, errors)


    def delegate_content_to_delete(self, user, session, request, context_list):
        """Delegates user's contents to superadmin (id=1) from list of context passed 
            by parameter context_list. Only do that if admin_new_owner is given as arg"""

        errors = []
        for content_context in context_list:
            content = session.query(content_context).filter_by(user_id=user.id).first()
            if content:
                if 'admin_new_owner' in request.args and request.args['admin_new_owner'] == '1':
                    contents = session.query(content_context).filter_by(user_id=user.id).all()
                    for c in contents:
                        admin = session.query(User).filter_by(id=1).first()
                        if admin:
                            c.user_id = admin.id
                        else:
                            errors.append('Could not find the super admin user.')
                else:
                    errors.append('You cannot delete this User because it has related ' + content_context.__tablename__)

        return True if not errors else  ErrorHandler().get_error(406, errors)