import os
import subwrap
from .utils import temp_filename, make_tar_with_metadata


class AppContainerImageWriter(object):
    @classmethod
    def new(cls):
        return cls()

    def create(self, source, destination, metadata):
        """Creates an app container image"""
        temp_image_filename = temp_filename()
        subwrap.run(['mksquashfs', source, temp_image_filename])

        make_tar_with_metadata(metadata, temp_image_filename, destination)
        os.remove(temp_image_filename)
