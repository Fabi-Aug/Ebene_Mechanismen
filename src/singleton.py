def singleton(cls):
    """
    A singleton decorator that stores the instance as a class attribute,
    and adds a clear_instance method to reset it.
    """
    original_new = cls.__new__
    instance = None

    def new_new(cls, *args, **kwargs):
        nonlocal instance
        if instance is None:
            if original_new is object.__new__:
                instance = original_new(cls)
            else:
                instance = original_new(cls, *args, **kwargs)
            cls._singleton_instance = instance  # store on the class
        return instance

    cls.__new__ = new_new
    cls.get_instance = classmethod(lambda cls: getattr(cls, "_singleton_instance", None))
    cls.clear_instance = classmethod(lambda cls: setattr(cls, "_singleton_instance", None))
    return cls
