from app import app, logHandler

class ErrorHandler(object):

    def __init__(self, error_code, error_message):
        if (type(error_message) == list or type(error_message) == str):
            error = error_message
        else:
            error = str(error_message)

        if (error_code == 500):
            app.logger.error(str(error))
        else:
            app.logger.info(str(error))

        #logHandler.doRollover()

        self.response = {
            'error': error_code,
            'message': error
        }, error_code