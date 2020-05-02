from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException
from app import errorHandler

from Models import Session, Variable, VariableSchema
from Validators import VariableValidator
from Utils import Paginate

class VariableRepository():
    
    def get(self):

        session = Session()
        schema = VariableSchema(many=True)
        
        try:
            query = session.query(Variable)
            result = Paginate(query, 1, 10)

            data = schema.dump(result.items)
            return {
                'data': data
            }, 200

        except SQLAlchemyError as e:
            return errorHandler.error_500_handler(e)

        except AttributeError as e:
            return errorHandler.error_400_handler(e)

        except HTTPException as e:
            return errorHandler.error_500_handler(e)

        finally:
            session.close()


    def get_by_id(self, id):

        session = Session()
        schema = VariableSchema(many=False)

        try:

            result = session.query(Variable).filter_by(id=id).first()
            data = schema.dump(result)

            if (data):
                return {
                    'data': data
                }, 200
            else:
                return errorHandler.error_404_handler('No Variable found.')

        except SQLAlchemyError as e:
            return errorHandler.error_500_handler(e)

        except HTTPException as e:
            return errorHandler.error_500_handler(e)

        finally:
            session.close()

    
    def create(self, request):

        data = request.get_json()

        if (data):

            validator = VariableValidator(data)
            
            if (validator.is_valid()):

                session = Session()

                try:
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
                    
                except SQLAlchemyError as e:
                    session.rollback()
                    return errorHandler.error_500_handler(e)

                except HTTPException as e:
                    session.rollback()
                    return errorHandler.error_500_handler(e)
                    
                finally:
                    session.close()
            
            else:
                return errorHandler.invalid_request_handler(validator.get_errors())

        else:
            return errorHandler.no_data_send_handler()


    def update(self, id, request):

        data = request.get_json()

        if (data):

            validator = VariableValidator(data)

            if (validator.is_valid()):

                session = Session()

                try:

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
                        return errorHandler.error_404_handler('No Variable found.')

                except SQLAlchemyError as e:
                    session.rollback()
                    return errorHandler.error_500_handler(e)

                except HTTPException as e:
                    session.rollback()
                    return errorHandler.error_500_handler(e)
                    
                finally:
                    session.close()

            else:
                return errorHandler.invalid_request_handler(validator.get_errors())

        else:
            return errorHandler.no_data_send_handler()


    def delete(self, id):

        session = Session()

        variable = Session.query(Variable).filter_by(id=id).first()

        if (variable):

            try:
                session.delete(variable)
                session.commit()

                return {
                    'message': 'Variable deleted successfully.',
                    'id': id
                }, 200

            except SQLAlchemyError as e:
                session.rollback()
                return errorHandler.error_500_handler(e)

            except HTTPException as e:
                session.rollback()
                return errorHandler.error_500_handler(e)
                
            finally:
                session.close()
        
        else:
            return errorHandler.error_404_handler('No Variable found.')