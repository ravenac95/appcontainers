import os
import shutil


class DirectoryList(object):
    def __init__(self, directories=None):
        self._directories = directories or []

    def append(self, directory):
        self._directories.append(directory)

    def __iter__(self):
        return iter(self._directories)

    def destroy(self):
        for directory in self._directories:
            directory.destroy()

    def as_paths(self):
        return map(lambda a: a.path, self._directories)


class BaseDirectory(object):
    def __init__(self, path):
        self._path = path

    @property
    def path(self):
        return self._path

    def destroy(self):
        raise NotImplementedError('destroy method is not implemented for '
                '"%s" class' % self.__class__.__name__)


class Directory(BaseDirectory):
    @classmethod
    def make(cls, path):
        """Creates a new directory"""
        abs_path = os.path.abspath(path)
        os.mkdir(abs_path)
        return cls(abs_path)

    def destroy(self):
        shutil.rmtree(self.path)


class SharedDirectory(BaseDirectory):
    """A directory that is not destroyed."""
    def destroy(self):
        pass
