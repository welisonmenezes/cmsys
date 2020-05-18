import datetime
import base64
from slugify import slugify
from app import app
from Decorators import SingletonDecorator

@SingletonDecorator
class Helper():
    """Utility class to get various desired values correctly and validated."""

    def get_date_from_string(self, str_date):
        """Converts the given string to a valid datetime and returns it or raise an Exception."""

        try:
            return datetime.datetime.strptime(str_date, '%Y-%m-%dT%H:%M:%S')
        except:
            raise Exception('Invalid format date. It must be like \'0000-00-00 00:00:00\'')

    
    def get_current_datetime(self):
        """Returns the current datetime"""

        return datetime.datetime.now()


    def get_base64_size(self, b64string):
        """Calculates the size of a given base64 string and returns its result."""

        try:
            file_info = self.get_file_type_and_data(b64string)
            size = (len(file_info[1]) * 3) / 4 - file_info[1].count('=', -2)
            return int(size)
        except Exception:
            raise Exception('The application could not get the file size.')


    def get_file_type_and_data(self, b64string):
        """Returns from given base64 string its type and its real data as a tuple."""

        header, data = b64string.split(',', 1)
        header = header.replace('data:','').replace(';base64','')
        tpl = (header, data)
        if (tpl and type(tpl) is tuple and tpl[0] != None and tpl[1] != None):
            return tpl
        else:
            raise Exception('The application has returned a invalid file type.')


    def get_extension_by_type(self, type):
        """Returns form given type the existing extension at dictionary located at app config file."""

        mime_types = app.config['VALID_MIMETYPES']
        try:
            return mime_types[type]
        except Exception:
            raise Exception('There is no compatible extension corresponding to the type: ' + type)


    def get_valid_mimetypes(self):
        """Returns all valid mimetypes registered at app config file."""

        mimitypes = app.config['VALID_MIMETYPES']
        return mimitypes.keys()


    def get_valid_extensions(self):
        """Returns all valid extensions registered at app config file."""

        extensions = app.config['VALID_MIMETYPES']
        return extensions.values()


    def get_file_details_from_request(self, data):
        """Separates the mimetype and the real base64 data from sended base64 data
            and returns it as a dictonary item."""
        
        try:
            type_and_data = self.get_file_type_and_data(data['file'])
            file_details = {
                'type': type_and_data[0],
                'data': base64.b64decode(type_and_data[1])
            }
            return file_details
        except:
            raise Exception('Cannot get file details. Please, check if it is a valid base64 file.')

    
    def get_null_if_empty(self, value):
        """Returns the value if it is not empty, otherwise, returns None."""

        return None if value == '' else value


    def get_with_slug(self, data, key):
        """Return the given dict data with value of the given key with slugfy applied."""

        if 'name' in data:
            data['name'] = slugify(data['name'])
        
        return data