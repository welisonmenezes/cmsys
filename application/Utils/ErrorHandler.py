from app import app
from Decorators import SingletonDecorator

@SingletonDecorator
class ErrorHandler(object):

    def get_error(self, error_code, error_message):
        if (type(error_message) == list or type(error_message) == str):
            error = error_message
        else:
            error = str(error_message)

        if (error_code == 500):
            app.logger.error(str(error))
        else:
            app.logger.info(str(error))

        return {
            'error': error_code,
            'message': error
        }, error_code