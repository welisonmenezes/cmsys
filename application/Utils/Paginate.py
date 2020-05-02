import math

class Paginate(object):

    def __init__(self, query, page, size):

        if page <= 0:
            raise AttributeError('page needs to be >= 1')

        if size <= 0:
            raise AttributeError('size needs to be >= 1')

        items = query.limit(size).offset((page - 1) * size).all()

        self.items = items
        self.build_pagination_infos(query, items, page, size)

        
    def build_pagination_infos(self, query, items, page, size):

        prev_items = (page - 1) * size
        total = query.order_by(None).count()
        prev = None
        next = None
        has_prev = page > 1
        has_next = prev_items + len(items) < total
        pages = int(math.ceil(total / float(size)))

        if has_prev:
            prev = page - 1
            
        if has_next:
            next = page + 1
            
        self.pagination = {
            'current': page,
            'prev': prev,
            'next': next,
            'has_prev': has_prev,
            'has_next': has_next,
            'size': size,
            'pages': pages,
            'total': total
        }