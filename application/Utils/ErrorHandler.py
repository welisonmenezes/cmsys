class ErrorHandler(object):

    @staticmethod
    def error_500_handler(e):
        error = str(e)
        return {
            'error': 500,
            'message': error
        }, 500


    @staticmethod
    def error_400_handler(e):
        error = str(e)
        return {
            'error': 400,
            'message': error
        }, 400


    @staticmethod
    def error_404_handler(message):
        return {
            'error': 404,
            'message': message
        }, 404


    @staticmethod
    def invalid_request_handler(errors):
        return {
            'error': 400,
            'errors': errors
        }, 400


    @staticmethod
    def no_data_send_handler():
        return {
            'error': 400,
            'message': 'No data send.'
        }, 400