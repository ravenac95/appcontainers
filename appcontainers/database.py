from ZODB import FileStorage, DB
import transaction


class Session(object):
    """Wrapper for the transaction"""
    def commit(self):
        transaction.commit()


class LocalDatabase(object):
    """Facade to ZODB database"""
    @classmethod
    def connect(cls, path):
        storage = FileStorage.FileStorage(path)
        database = DB(storage)
        connection = database.open()
        return cls(connection, database, storage)

    def __init__(self, connection, database, storage):
        self._connection = connection
        self._database = database
        self._storage = storage

    @property
    def root(self):
        return self._connection.root()

    def close(self):
        self._connection.close()
        self._database.close()
        self._storage.close()
