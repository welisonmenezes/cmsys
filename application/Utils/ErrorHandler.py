class ErrorHandler():

    def error_500_handler(self, e):
        error = str(e)
        return {
            'error': 500,
            'message': error
        }, 500

    
    def error_400_handler(self, e):
        error = str(e)
        return {
            'error': 400,
            'message': error
        }, 400


    def error_404_handler(self, message):
        return {
            'error': 404,
            'message': message
        }, 404

    
    def invalid_request_handler(self, errors):
        return {
            'error': 400,
            'errors': errors
        }, 400


    def no_data_send_handler(self):
        return {
            'error': 400,
            'message': 'No data send.'
        }, 400