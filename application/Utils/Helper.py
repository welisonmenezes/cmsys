import datetime

class Helper():

    @staticmethod
    def get_date_from_string(str_date):
        try:
            return datetime.datetime.strptime(str_date, '%Y-%m-%dT%H:%M:%S')
        except:
            raise Exception('Invalid format date. It must be like \'0000-00-00 00:00:00\'')