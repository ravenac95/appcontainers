import os
import subwrap
import tarfile
import json
import time
from cStringIO import StringIO
from .utils import temp_filename


class AppContainerImageBuilder(object):
    def __init__(self, image_name, overlay_path, image_path, tar_type='gz'):
        self._image_name = image_name
        self._overlay_path = overlay_path
        self._image_path = image_path
        self._tar_type = tar_type
        self._tar = None

    def start(self):
        self._tar = tarfile.open(self._image_path, 'w:%s' % self._tar_type)

    def tarfile_path(self, *joins):
        path = os.path.join(self._image_name, *joins)
        return path

    def add_metadata(self, metadata):
        metadata_filename = self.tarfile_path('metadata.json')
        metadata_str = json.dumps(metadata)
        metadata_info = tarfile.TarInfo(metadata_filename)
        metadata_info.size = len(metadata_str)
        metadata_info.mtime = int(time.time())
        metadata_file = StringIO(metadata_str)
        self._tar.addfile(metadata_info, fileobj=metadata_file)

    def compress_fs(self):
        temp_image_filename = temp_filename()

        # Create squashfs
        subwrap.run(['mksquashfs', self._overlay_path, temp_image_filename])

        # Create the tarinfo to describe the location in the archive
        tarfile_name = self.tarfile_path('app.sqsh')

        # Load the file into the tarfile using the tarinfo above
        image_info = self._tar.gettarinfo(arcname=tarfile_name,
                name=temp_image_filename)
        self._tar.addfile(image_info)

        # Clean up
        os.remove(temp_image_filename)

    def finished(self):
        self._tar.close()
        return self._image_path


class AppContainerImageWriter(object):
    """Director of the image writer"""
    def setup_builder(self, container, image_path, image_name):
        overlay_path = container.image_point()
        builder = AppContainerImageBuilder(image_name, overlay_path,
                image_path)
        return builder

    def create(self, container, image_path, image_name=None):
        """Creates an app container image"""
        metadata = dict(base=container.base)
        image_name = image_name or container.name

        builder = self.setup_builder(container, image_path, image_name)
        builder.start()
        builder.add_metadata(metadata)
        builder.compress_fs()
        image_path = builder.finished()

        return image_path
