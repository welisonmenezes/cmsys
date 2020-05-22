class BadRequestError(Exception):

    def __init__(self, message):
        super(Exception, self).__init__(str(message))
        self.message = message