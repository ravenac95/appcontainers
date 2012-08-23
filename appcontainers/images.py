import os
import subwrap
import tarfile
import json
import time
from cStringIO import StringIO
from .utils import temp_filename
from . import constants


class AppContainerImageBuilder(object):
    def __init__(self, source, destination_dir, image_name, tar_type='w:gz'):
        self._image_name = image_name
        self._destination_dir = destination_dir
        self._source = source
        self._tar_type = tar_type
        self._tar_filename = '%s.%s' % (image_name,
                constants.IMAGE_FILE_EXTENSION)
        self._tar = None

    def start(self):
        tarfile_dest = os.path.join(self._destination_dir,
                self._tar_filename)
        self._tar = tarfile.open(tarfile_dest, 'w:gz')

    def add_metadata(self, metadata):
        metadata_filename = self.tarfile_path('metadata.json')
        metadata_str = json.dumps(metadata)
        metadata_info = tarfile.TarInfo(metadata_filename)
        metadata_info.size = len(metadata_str)
        metadata_info.mtime = int(time.time())
        metadata_file = StringIO(metadata_str)
        self._tar.addfile(metadata_info, fileobj=metadata_file)

    def add_image(self, temp_image_filename):
        tarfile_name = self.tarfile_path('app.sqsh')
        image_info = self._tar.gettarinfo(arcname=tarfile_name,
                name=temp_image_filename)
        self._tar.addfile(image_info)

    def close(self):
        self._tar.close()

    def tarfile_path(self, *joins):
        path = os.path.join(self._image_name, *joins)
        return path


class AppContainerImageWriter(object):
    @classmethod
    def new(cls):
        return cls()

    def create(self, source, destination_dir, dest_image_name, metadata):
        """Creates an app container image"""
        temp_image_filename = temp_filename()
        subwrap.run(['mksquashfs', source, temp_image_filename])

        builder = AppContainerImageBuilder(source, destination_dir,
                dest_image_name)
        builder.start()
        builder.add_metadata(metadata)
        builder.add_image(temp_image_filename)
        builder.close()

        os.remove(temp_image_filename)
