import datetime
#import filetype
import base64
#import magic
import mimetypes

class Helper():

    @staticmethod
    def get_date_from_string(str_date):
        try:
            return datetime.datetime.strptime(str_date, '%Y-%m-%dT%H:%M:%S')
        except:
            raise Exception('Invalid format date. It must be like \'0000-00-00 00:00:00\'')


    @staticmethod
    def get_base64_size(b64string):
        size = (len(b64string) * 3) / 4 - b64string.count('=', -2)
        return int(size)


    @staticmethod
    def get_file_type_and_data(b64string):
        header, data = b64string.split(',', 1)
        header = header.replace('data:','').replace(';base64','')
        tpl = (header, data)
        if (tpl and type(tpl) is tuple and tpl[0] != None and tpl[1] != None):
            return tpl
        else:
            raise Exception('The application has returned a invalid file type.')


    @staticmethod
    def get_extension_by_type(type):
        mime_types = {
            'text/plain': 'txt',
            'image/png': 'png',
            'image/jpeg': 'jpeg',
            'image/jpg': 'jpg',
            'image/gif': 'gif',
            'image/bmp': 'bmp',
            'image/vnd.microsoft.icon': 'ico',
            'image/svg+xml': 'svg',
            'image/svg+xml': 'svgx',
            'application/zip': 'zip',
            'application/x-rar-compressed': 'rar',
            'audio/mpeg': 'mp3',
            'audio/ogg': 'ogg',
            'video/quicktime': 'qt',
            'video/quicktime': 'mov',
            'application/octet-stream': 'docx',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
            'application/msword': 'doc',
            'application/rtf': 'rtf',
            'application/vnd.ms-excel': 'xls',
            'application/vnd.ms-powerpoint': 'ppt',
            'text/javascript': 'js',
            'application/json': 'json',
            'text/html': 'html',
            'text/css': 'css',
            'text/csv': 'csv'
        }
        try:
            return mime_types[type]
        except Exception:
            raise Exception('There is no compatible extension corresponding to the type: ' + type)

