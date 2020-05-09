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
            return ErrorHandler().get_error().get_error(500, e)

        except AttributeError as e:
            if (need_rollback):
                session.rollback()
            return ErrorHandler().get_error(400, e)

        except HTTPException as e:
            if (need_rollback):
                session.rollback()
            return ErrorHandler().get_error(500, e)
            
        finally:
            session.close()

    
    def get_existing_foreing_id(self, data, key, context, session, get_all_filelds= False):
        if (key in data):
            if (get_all_filelds):
                element = session.query(context).filter_by(id=int(data[key])).first()
            else:
                element = session.query(getattr(context, 'id')).filter_by(id=int(data[key])).first()
                
            if (element):
                return element if get_all_filelds else element.id
            else:
                raise Exception('Cannont find '+ str(context.__tablename__) + ': ' + str( data[key]))