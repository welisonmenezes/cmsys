import math

class Paginate(object):

    def __init__(self, query, page, page_size):

        if page <= 0:
            raise AttributeError('page needs to be >= 1')
        if page_size <= 0:
            raise AttributeError('page_size needs to be >= 1')

        items = query.limit(page_size).offset((page - 1) * page_size).all()
        previous_items = (page - 1) * page_size
        total = query.order_by(None).count()


        self.items = items
        self.previous_page = None
        self.next_page = None
        self.has_previous = page > 1
        self.has_next = previous_items + len(items) < total

        if self.has_previous:
            self.previous_page = page - 1
            
        if self.has_next:
            self.next_page = page + 1

        self.total = total
        self.pages = int(math.ceil(total / float(page_size)))