class ErrorHandler():

    def error500Handler(self, e):
        error = str(e)
        return {
            'message': error
        }, 500


    def error404Handler(self, message):
        return {
            'message': message
        }, 404