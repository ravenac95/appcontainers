import os
import tempfile


def make_tar_with_metadata(metadata, temp_image_filename, destination):
    #tarfile.TarInfo(
    pass


def temp_filename(*args):
    handle, filename = tempfile.mkstemp()
    os.close(handle)
    os.remove(filename)
    return filename
