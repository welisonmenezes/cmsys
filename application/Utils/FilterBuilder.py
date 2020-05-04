from Utils import Checker

class FilterBuilder():

    def __init__(self, context, args):
        self.filter = ()
        self.context = context
        self.args = args
        self.page = 1
        self.limit = 10


    def set_equals_filter(self, key):
        if (self.args[key]):
            self.filter += (getattr(self.context, key) == self.args[key],)

    
    def set_like_filter(self, key):
        if (self.args[key]):
            self.filter += (getattr(self.context, key).like('%' + self.args[key] + '%'),)

    
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
