from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException
from sqlalchemy import or_
from Utils import Checker
from Models import Session, Media, FieldFile, FieldText, FieldContent
from ErrorHandlers import ErrorHandler, BadRequestError, NotFoundError

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

        except BadRequestError as e:
            if (need_rollback):
                session.rollback()
            return ErrorHandler().get_error(400, e.message)
        
        except NotFoundError as e:
            if (need_rollback):
                session.rollback()
            return ErrorHandler().get_error(404, e.message)

        except SQLAlchemyError as e:
            if (need_rollback):
                session.rollback()
            return ErrorHandler().get_error(500, str(e))

        except HTTPException as e:
            if (need_rollback):
                session.rollback()
            return ErrorHandler().get_error(500, str(e))

        except AttributeError as e:
            if (need_rollback):
                session.rollback()
            return ErrorHandler().get_error(500, str(e))

        except Exception as e:
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
                raise BadRequestError(validator.get_errors())

        else:
            raise BadRequestError('No data sent.')


    def run_if_exists(self, fn, context, id, session):
        """Runs the given method if the given element exists at the database."""

        element = session.query(context).filter_by(id=id).first()
        if (element):
            return fn(session, element)
        else:
            raise NotFoundError('No ' + context.__tablename__ + ' found.')


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
            raise Exception('Invalid success error handler parameters.')


    def get_suggestions(self, name, context, session):
        """Returns names suggestions to given context from given initial name."""

        initial_name = searchable_name = name
        suggestion_index = index = total_index = 0
        suggestions = []
        
        while index < 10 and total_index < 100:
            result = session.query(getattr(context, 'name')).filter_by(name=searchable_name).first()
            
            if result:
                suggestion_index += 1
                searchable_name = initial_name + '-' + str(suggestion_index)
            else:
                if not searchable_name in suggestions:
                    suggestions.append(searchable_name)
                    index += 1
                    suggestion_index += 1
                else:
                    searchable_name = initial_name + '-' + str(suggestion_index)
            
            total_index += 1

        return {
            'suggestions': suggestions
        }, 200


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
                raise NotFoundError('Cannont find '+ str(context.__tablename__) + ': ' + str( data[key]))


    def is_foreigners(self, configurations, session):
        """Verifies if is a foreigner on any given context at configuration, if so, return errors. How to use:
            The configuration must like: [(current_context, foreign_key_at_target_context, target_context)]"""

        errors = []
        for config in configurations:
            filter = (getattr(config[2], config[1])==getattr(config[0], 'id'),)
            element = session.query(getattr(config[2], 'id')).filter(*filter).first()
            if element:
                errors.append('You cannot delete this ' + config[0].__class__.__name__ + ' because it has a related ' + config[2].__tablename__)

        if errors:
            raise BadRequestError(errors)

    def add_foreign_keys(self, current_context, data, session, configurations):
        """Controls if the list of foreign keys is an existing foreign key data. How to use:
            The configurtations must like: [('foreign_key_at_target_context, target_context)]"""

        errors = []
        for config in configurations:
            try:
                setattr(current_context, config[0], self.get_existing_foreing_id(data, config[0], config[1], session))
            except Exception as e:
                errors.append('Could not find the given foreign key \'' + str(config[0]) + '\'')

        if errors:
            raise BadRequestError(errors)


    def set_any_reference_as_null_to_delete(self, instance, request, session, configurations):
        """Sets the given foreign key at the given Model as None to allow delete the given instance.
            Note that this only occurs if the 'remove_foreign_key' passed by request param was equals 1.
            How to use: The configuration must like: [(foreign_key_at_target_context, target_context)]"""

        errors = []
        for config in configurations:
            try:
                if 'remove_foreign_keys' in request.args and request.args['remove_foreign_keys'] == '1':
                    filter = (getattr(config[1], config[0])==instance.id,)
                    elements = session.query(config[1]).filter(*filter).all()
                    for element in elements:
                        setattr(element, config[0], None)
                else:
                    filter = (getattr(config[1], config[0])==instance.id,)
                    element = session.query(getattr(config[1], 'id')).filter(*filter).first()
                    if element:
                        errors.append('You cannot delete this ' + instance.__class__.__name__ + ' because it has a related ' + config[1].__tablename__)

            except Exception as e:
                errors.append(str(e))

        if errors:
            raise BadRequestError(errors)


    def set_children_as_null_to_delete(self, instance, context, session):
        """Sets the children of the given instance as null to we can delete it."""

        child = session.query(getattr(context, 'id')).filter_by(parent_id=instance.id).first()
        if child:
            children = session.query(context).filter_by(parent_id=instance.id).update(values={'parent_id': None}, synchronize_session='evaluate')


    def add_many_to_many_relationship(self, key, instance, data, context_target, session):
        """From the given key get from the given data the list of context_target id
            to add into the given instance"""

        if (key in data and isinstance(data[key], list)):

            errors = []
            for related in data[key]:
                if (related and Checker().can_be_integer(related)):
                    registered_related = session.query(context_target).filter_by(id=int(related)).first()
                    if (registered_related):
                        getattr(instance, key).append(registered_related)
                    else:
                        errors.append(context_target.__tablename__ + ' ' + str(related) + ' does not exists.')

            if errors:
                raise NotFoundError(errors)


    def edit_many_to_many_relationship(self, key, instance, data, context_target, session):
        """From the given key get from the given data the list of context_target id
            to add/remove into the given instance"""

        old_relateds = []
        new_old_relateds = []

        if (getattr(instance, key)):
            for related in getattr(instance, key):
                old_relateds.append(related.id)

        if (key in data and isinstance(data[key], list)):
            for related in data[key]:
                if (related and Checker().can_be_integer(related)):
                    new_old_relateds.append(related)

        related_to_delete = list(set(old_relateds) - set(new_old_relateds))
        related_to_add = list(set(new_old_relateds) - set(old_relateds))

        for related in related_to_delete:
            registered_related = session.query(context_target).filter_by(id=int(related)).first()
            if (registered_related):
                getattr(instance, key).remove(registered_related)
        
        for related in related_to_add:
            registered_related = session.query(context_target).filter_by(id=int(related)).first()
            if (registered_related):
                getattr(instance, key).append(registered_related)


    def raise_if_has_different_parent_reference(self, data, session, configurations):
        """Verify if the given data has the same foreign data that its parent. How to use:
            The configuration must like: [('parent_key','referenced_key', 'context_target')]"""

        errors = []
        for config in configurations:
            try:
                if config[0] in data and config[1] in data:
                    parent = session.query(getattr(config[2], config[1])).filter_by(id=int(data[config[0]])).first()
                    if parent and parent[0] != int(data[config[1]]):
                        errors.append('The ' + config[1] + ' must be the same as your father\'s, witch is: ' + str(parent[0]) + '.')
            except Exception as e:
                errors.append(str(e))

        if errors:
            raise BadRequestError(errors)


    def delete_deep_chidren(self, parent, context, session):
        """Delete children deeply from a given parent."""
        
        children = session.query(context).filter_by(parent_id=getattr(parent, 'id')).all()
        if children:
            for child in children:
                self.delete_deep_chidren(child, context, session)
                session.delete(child)


    def delete_children(self, session, id, configurations):
        """Delete the Field children. Attention to cascading order. How to use: 
            The configurations must like: [(target_key, target_context)]"""

        for config in configurations:
            print(config)
            filter = (getattr(config[1], config[0])==id,)
            session.query(config[1]).filter(*filter).delete(synchronize_session='evaluate')


    def add_foreign_keys_field_type(self, field_type, current_context, data, session, configurations, id=None):
        """Controls if the list of foreign keys is an existing foreign key data. How to use:
            The configurtations must like: [('foreign_key_at_target_context, target_context)]"""

        errors = []
        for config in configurations:
            try:
                if config[0] == 'field_id':
                    el = self.get_existing_foreing_id(data, config[0], config[1], session, True)

                    if el:
                        
                        if el.type != field_type:
                            errors.append('The Field referenced by the \'field_id\' is not configured as ' + field_type + '.')

                        if not id or (data['field_id'] != current_context.field_id):
                            filter = (or_(FieldContent.field_id==el.id, FieldText.field_id==el.id, FieldFile.field_id==el.id),)
                            el_childs = session.query(FieldContent.id, FieldFile.id, FieldText.id).filter(*filter).first()
                        
                            if el_childs:
                                errors.append('The Field referenced by the \'field_id\' already has a field type.')

                setattr(current_context, config[0], self.get_existing_foreing_id(data, config[0], config[1], session))
            except Exception as e:
                errors.append('Could not find the given foreign key \'' + str(config[0]) + '\'')

        if errors:
            raise BadRequestError(errors)