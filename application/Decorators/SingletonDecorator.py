from functools import wraps

def SingletonDecorator(cls):
    """Decorator to implement the singleton pattern to its members."""

    instances = {}
    @wraps(cls)

    def instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
        
    return instance