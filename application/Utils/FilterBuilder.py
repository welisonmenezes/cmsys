from sqlalchemy import desc, asc, not_
from Utils import Checker, Helper

class FilterBuilder():

    def __init__(self, context, args):
        self.filter = ()
        self.context = context
        self.args = args
        self.page = 1
        self.limit = 10


    def get_context_attr(self, key, kwa):
        if ('joined' in kwa and 'joined_key' in kwa):
            return getattr(kwa['joined'], kwa['joined_key'])
        else:
            return getattr(self.context, key)


    def set_equals_filter(self, key, *args, **kwargs):
        if (self.args[key]):
            self.filter += (self.get_context_attr(key, kwargs) == self.args[key], )

    
    def set_like_filter(self, key, *args, **kwargs):
        if (self.args[key]):
            self.filter += (self.get_context_attr(key, kwargs).like('%' + self.args[key] + '%'), )

    
    def set_date_filter(self, key, *args, **kwargs):
        if (self.args[key]):
            try:
                date_time = Helper.get_date_from_string(self.args[key])

                date_modifier = 'greater_or_equal'
                if ('date_modifier' in kwargs and kwargs['date_modifier']):
                        date_modifier = kwargs['date_modifier']

                if (date_modifier == 'greater'):
                    self.filter += (self.get_context_attr(key, kwargs) > date_time,)
                elif (date_modifier == 'less'):
                    self.filter += (self.get_context_attr(key, kwargs) < date_time,)
                elif (date_modifier == 'greater_or_equal'):
                    self.filter += (self.get_context_attr(key, kwargs) >= date_time,)
                elif (date_modifier == 'less_or_equal'):
                    self.filter += (self.get_context_attr(key, kwargs) <= date_time,)
                elif (date_modifier == 'equal'):
                    self.filter += (self.get_context_attr(key, kwargs) == date_time,)
                elif (date_modifier == 'different'):
                    self.filter += (self.get_context_attr(key, kwargs) != date_time,)
                else:
                    raise Exception('The parameter \'date_modifier\' must be one of these: [greater, less, greater_or_equal, less_or_equal, equal or different]')

            except Exception as e:
                raise Exception(str(e))


    def set_between_dates_filter(self, key, *args, **kwargs):
        try:
            if ('compare_date_time_one' in kwargs and 'compare_date_time_two' in  kwargs 
                and kwargs['compare_date_time_one'] and kwargs['compare_date_time_two']):
                date_time_one = Helper.get_date_from_string(kwargs['compare_date_time_one'])
                date_time_two = Helper.get_date_from_string(kwargs['compare_date_time_two'])

                if ('not_between' in kwargs and kwargs['not_between'] == '1'):
                    self.filter += (not_(self.get_context_attr(key, kwargs).between(date_time_one, date_time_two)),)
                else:
                    self.filter += (self.get_context_attr(key, kwargs).between(date_time_one, date_time_two),)

        except Exception as e:
            raise Exception(str(e))

    
    def get_filter(self):
        return self.filter


    def get_page(self):
        if (self.args['page'] and Checker().can_be_integer(self.args['page'])):
            self.page = int(self.args['page'])
        return self.page


    def get_limit(self):
        if (self.args['limit'] and Checker().can_be_integer(self.args['limit'])):
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