def singleton(cls):
    instances = {}
    def wrapper(*args, **kwargs):
        if cls not in instances:
            # Create a new instance if it doesn't exist
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper