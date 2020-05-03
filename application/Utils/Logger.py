import logging, os
import logging.handlers as handlers

class Logger():

    def __init__(self, app):
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logHandler = handlers.RotatingFileHandler(os.path.abspath('log/log.log'), maxBytes=1048576, backupCount=3, encoding=None, delay=True)
        logHandler.setLevel(logging.NOTSET)
        logHandler.setFormatter(formatter)
        app.logger.addHandler(logHandler)
        app.logger.debug('Aplication started!')