from sqlalchemy import desc, asc
from Utils import Checker, Helper

class FilterBuilder():

    def __init__(self, context, args):
        self.filter = ()
        self.context = context
        self.args = args
        self.page = 1
        self.limit = 10


    # TODO: implement functionality to filter data between two dates


    def set_equals_filter(self, key, *args, **kwargs):
        if (self.args[key]):
            if ('joined' in kwargs and 'joined_key' in kwargs):
                self.filter += (getattr(kwargs['joined'], kwargs['joined_key']) == self.args[key],)
            else:
                self.filter += (getattr(self.context, key) == self.args[key],)

    
    def set_like_filter(self, key, *args, **kwargs):
        if (self.args[key]):
            if ('joined' in kwargs and 'joined_key' in kwargs):
                self.filter += (getattr(kwargs['joined'], kwargs['joined_key']).like('%' + self.args[key] + '%'),)
            else:
                self.filter += (getattr(self.context, key).like('%' + self.args[key] + '%'),)

    
    def set_date_filter(self, key, *args, **kwargs):
        if (self.args[key]):
            date_time_obj = Helper.get_date_from_string(self.args[key])
            try:
                date_time_obj = Helper.get_date_from_string(self.args[key])

                date_modifier = 'greater_or_equal'
                if (kwargs['date_modifier']):
                    date_modifier = kwargs['date_modifier']

                if ('joined' in kwargs and 'joined_key' in kwargs):
                    if (date_modifier == 'greater'):
                        self.filter += (getattr(kwargs['joined'], kwargs['joined_key']) > date_time_obj,)
                    elif (date_modifier == 'less'):
                        self.filter += (getattr(kwargs['joined'], kwargs['joined_key']) < date_time_obj,)
                    elif (date_modifier == 'greater_or_equal'):
                        self.filter += (getattr(kwargs['joined'], kwargs['joined_key']) >= date_time_obj,)
                    elif (date_modifier == 'less_or_equla'):
                        self.filter += (getattr(kwargs['joined'], kwargs['joined_key']) <= date_time_obj,)
                    elif (date_modifier == 'equal'):
                        self.filter += (getattr(kwargs['joined'], kwargs['joined_key']) == date_time_obj,)
                    elif (date_modifier == 'different'):
                        self.filter += (getattr(kwargs['joined'], kwargs['joined_key']) != date_time_obj,)
                    else:
                        raise Exception('The parameter \'date_modifier\' must be one of these: [greater, less, greater_or_equal, less_or_equal, equal or different]')
                else:
                    if (date_modifier == 'greater'):
                        self.filter += (getattr(self.context, key) > date_time_obj,)
                    elif (date_modifier == 'less'):
                        self.filter += (getattr(self.context, key) < date_time_obj,)
                    elif (date_modifier == 'greater_or_equal'):
                        self.filter += (getattr(self.context, key) >= date_time_obj,)
                    elif (date_modifier == 'less_or_equal'):
                        self.filter += (getattr(self.context, key) <= date_time_obj,)
                    elif (date_modifier == 'equal'):
                        self.filter += (getattr(self.context, key) == date_time_obj,)
                    elif (date_modifier == 'different'):
                        self.filter += (getattr(self.context, key) != date_time_obj,)
                    else:
                        raise Exception('The parameter \'date_modifier\' must be one of these: [greater, less, greater_or_equal, less_or_equal, equal or different]')
            except Exception as e:
                raise Exception(e)
            
    
    def get_filter(self):
        return self.filter


    def get_page(self):
        if (self.args['page'] and Checker.can_be_integer(self.args['page'])):
            self.page = int(self.args['page'])
        return self.page


    def get_limit(self):
        if (self.args['limit'] and Checker.can_be_integer(self.args['limit'])):
            self.limit = int(self.args['limit'])
        return self.limit


    def get_order_by(self):
        if (self.args['order_by'] and self.args['order_by'] != ''):
            if (self.args['order'] and self.args['order'] == 'desc'):
                order_by = [desc(getattr(self.context, self.args['order_by']))]
            else:
                order_by = [asc(getattr(self.context, self.args['order_by']))]
        else:
            order_by = [desc(self.context.id)]
        return order_by
