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
            return ErrorHandler.error_500_handler(e)
        except AttributeError as e:
            if (need_rollback):
                session.rollback()
            return ErrorHandler.error_400_handler(e)
        except HTTPException as e:
            if (need_rollback):
                session.rollback()
            return ErrorHandler.error_500_handler(e)
        finally:
            session.close()