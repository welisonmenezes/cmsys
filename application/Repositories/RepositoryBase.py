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
            return ErrorHandler.error_handler(500, e)
        except AttributeError as e:
            if (need_rollback):
                session.rollback()
            return ErrorHandler.error_handler(400, e)
        except HTTPException as e:
            if (need_rollback):
                session.rollback()
            return ErrorHandler.error_handler(500, e)
        finally:
            session.close()