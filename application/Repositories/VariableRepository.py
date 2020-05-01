from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException
from app import app, errorHandler

from Models import Session, Variable, VariableSchema

class VariableRepository():
    
    def getAll(self):

        session = Session()
        schema = VariableSchema(many=True)
        
        try:
            result = session.query(Variable).all()
            data = schema.dump(result)
            return {
                'data': data
            }, 200

        except SQLAlchemyError as e:
            return errorHandler.error500Handler(e)

        except HTTPException as e:
            return errorHandler.error500Handler(e)

        finally:
            session.close()


    def getByID(self, id):

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
                return errorHandler.error404Handler('No Variable found.')

        except SQLAlchemyError as e:
            return errorHandler.error500Handler(e)

        except HTTPException as e:
            return errorHandler.error500Handler(e)

        finally:
            session.close()