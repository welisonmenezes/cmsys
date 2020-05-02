class ErrorHandler(object):

    @staticmethod
    def error_handler(error_code, error_message):
        if (type(error_message) == list or type(error_message) == str):
            error = error_message
        else:
            error = str(error_message)

        return {
            'error': error_code,
            'message': error
        }, error_code