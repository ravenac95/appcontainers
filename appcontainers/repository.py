class DoesNotExist(Exception):
    pass


class Repository(object):
    """A generic repository class"""
    DoesNotExist = DoesNotExist

    def __init__(self, database):
        self._database = database

    def all(self):
        raise NotImplementedError('"all" method not implemented')

    def save(self, obj):
        raise NotImplementedError('"save" method not implemented')
