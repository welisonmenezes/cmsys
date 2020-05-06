from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException
from Utils import ErrorHandler
from Models import Session

class RepositoryBase():

    def __init__(self):
        self.joins = []
        self.fields = []

    
    def response(self, fn, need_rollback):
        session = Session()

        try:
            return fn(session)

        except SQLAlchemyError as e:
            if (need_rollback):
                session.rollback()
            return ErrorHandler(500, e).response

        except AttributeError as e:
            if (need_rollback):
                session.rollback()
            return ErrorHandler(400, e).response

        except HTTPException as e:
            if (need_rollback):
                session.rollback()
            return ErrorHandler(500, e).response
            
        finally:
            session.close()

    
    def get_existing_foreing_id(self, data, key, context, session):
        if (key in data):
            element = session.query(getattr(context, 'id')).filter_by(id=int(data[key])).first()
            if (element):
                return element.id
            else:
                raise Exception('Cannont find '+ str(context.__tablename__) + ': ' + str( data[key]))