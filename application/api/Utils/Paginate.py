import math

class Paginate():
    """When instantiated generates a paginator to the given SqlAlchemy query."""

    def __init__(self, query, page, size):
        """Gets the SqlAlchemy query and apply on it the given page and size to generate the paginated result."""

        if page <= 0:
            raise Exception('page needs to be >= 1')

        if size <= 0:
            raise Exception('size needs to be >= 1')

        items = query.limit(size).offset((page - 1) * size).all()

        self.items = items
        self.pagination = self.get_pagination_infos(query, items, page, size)

        
    def get_pagination_infos(self, query, items, page, size):
        """Returns the properly formatted pagination infos. This method is called by the __init__ method above."""

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
            
        return {
            'current': page,
            'prev': prev,
            'next': next,
            'has_prev': has_prev,
            'has_next': has_next,
            'size': size,
            'pages': pages,
            'total': total
        }