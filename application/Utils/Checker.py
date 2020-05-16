import datetime
from datetime import date, timedelta
from app import app_config
from Decorators import SingletonDecorator

@SingletonDecorator
class Checker():
    """Utility class to make boolean various verifications across the application."""

    def can_be_integer(self, value):
        """Checks if a string value can be converted to integer."""

        try:
            int(value)
            return True
        except ValueError:
            return False


    def is_image_type(self, mimetype):
        """Checks if a string mimetype exists into app config as valid image mimetype."""
        
        image_types = app_config['IMAGE_MIMETYPES'].keys()
        return True if mimetype in image_types else False


    def is_datetime(self, str_datetime):
        """Checks if a given str datetime is a valid datetime."""

        datetime_format = '%Y-%m-%d %H:%M:%S'
        try:
            datetime.datetime.strptime(str_datetime, datetime_format)
            return True
        except ValueError:
            return False


    def is_first_date_smaller(self, publish_on, expire_on):
        """Checks if the first date passed by parameter is smaller than the second one."""

        try:
            publish_date, publish_time = publish_on.split(' ')
            publish_year, publish_month, publish_day = publish_date.split('-')
            publish_hour, publish_minute, publish_second = publish_time.split(':')
            publish_second = publish_second.split('.')[0]
            final_publish_on = datetime.datetime(int(publish_year), int(publish_month), int(publish_day), int(publish_hour), int(publish_minute), int(publish_second))

            expire_date, expire_time = expire_on.split(' ')
            expire_year, expire_month, expire_day = expire_date.split('-')
            expire_hour, expire_minute, expire_second = expire_time.split(':')
            expire_second = expire_second.split('.')[0]
            final_expire_on = datetime.datetime(int(expire_year), int(expire_month), int(expire_day), int(expire_hour), int(expire_minute), int(expire_second))
            final_expire_on = final_expire_on - timedelta(hours=1)

            if final_expire_on <= final_publish_on:
                return False
            else:
                return True
        except:
            raise Exception('The method \'is_first_date_smaller\' has failed during its process. Please, check if your arguments are correct.')