class Factory(object):
    _objects = {}

    @classmethod
    def has(cls,name):
        if name in cls._objects.keys():
            return True
        return False

    @classmethod
    def get(cls,name):
        if not cls.has(name):
            raise Exception('Invalid object name: ', name)

        return cls._objects[name]


    @classmethod
    def set(cls,name,obj):
        if cls.has(name):
            raise Exception('Object name already set: ', name)

        cls._objects[name] = obj