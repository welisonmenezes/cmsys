class ErrorHandler():

    def error_500_handler(self, e):
        error = str(e)
        return {
            'message': error
        }, 500


    def error_404_handler(self, message):
        return {
            'message': message
        }, 404