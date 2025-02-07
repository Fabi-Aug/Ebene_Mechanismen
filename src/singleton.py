# singleton.py

def singleton(cls):
    """
    Ein Singleton-Dekorator, der die Klassenidentität bewahrt und
    der dekorierten Klasse eine `get_instance`-Klassenmethode hinzufügt.
    """
    original_new = cls.__new__
    instance = None

    def new_new(cls, *args, **kwargs):
        nonlocal instance
        if instance is None:
            if original_new is object.__new__:
                # Falls original_new einfach object.__new__ ist,
                # rufe es nur mit cls auf.
                instance = original_new(cls)
            else:
                instance = original_new(cls, *args, **kwargs)
        return instance

    cls.__new__ = new_new
    cls.get_instance = classmethod(lambda cls: instance)
    return cls
