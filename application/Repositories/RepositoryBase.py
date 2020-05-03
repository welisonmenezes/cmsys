from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException
from Utils import ErrorHandler
from Models import Session

class RepositoryBase():
    
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