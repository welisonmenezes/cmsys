from functools import wraps

def SingletonDecorator(cls):
    instances = {}
    @wraps(cls)

    def instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
        
    return instance