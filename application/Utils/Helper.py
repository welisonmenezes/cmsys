import datetime
import base64
from app import app_config
from Decorators import SingletonDecorator

@SingletonDecorator
class Helper():

    def get_date_from_string(self, str_date):
        try:
            return datetime.datetime.strptime(str_date, '%Y-%m-%dT%H:%M:%S')
        except:
            raise Exception('Invalid format date. It must be like \'0000-00-00 00:00:00\'')


    def get_base64_size(self, b64string):
        size = (len(b64string) * 3) / 4 - b64string.count('=', -2)
        return int(size)


    def get_file_type_and_data(self, b64string):
        header, data = b64string.split(',', 1)
        header = header.replace('data:','').replace(';base64','')
        tpl = (header, data)
        if (tpl and type(tpl) is tuple and tpl[0] != None and tpl[1] != None):
            return tpl
        else:
            raise Exception('The application has returned a invalid file type.')


    def get_extension_by_type(self, type):
        mime_types = app_config['VALID_MIMETYPES']
        try:
            return mime_types[type]
        except Exception:
            raise Exception('There is no compatible extension corresponding to the type: ' + type)


    def get_valid_mimetypes(self):
        mimitypes = app_config['VALID_MIMETYPES']
        return mimitypes.keys()


    def get_valid_extensions(self):
        extensions = app_config['VALID_MIMETYPES']
        return extensions.values()