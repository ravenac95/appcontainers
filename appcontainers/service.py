import os
import time
from . import constants
from .images import AppContainerImageWriter


def create_app_container_object():
    return None

# Process for creating an app container
#
# Provision container with overlays
#  - Create overlay directory
#  - Mount overlay
#  - Setup skeleton files for this container instance
# Add app files to container
# Run build command in container
# Squash the container's raw overlay and save into the user images
# Clean the raw overlay


class AppContainerService(object):
    """The facade to dealing with app containers."""
    def __init__(self, resource_service, creator,
            base_path='/var/lib/appcontainers'):
        self._base_path = base_path
        self._creator = creator
        self._resource_service = resource_service

    def provision(self, base='base'):
        """Provision a new app container using the default base"""
        # Setup the information for the container
        resource_reservation = self._resource_service.make_reservation()
        app_container = self._creator.provision_container(base, resource_reservation)
        return ManagedAppContainer(self, app_container)

    def service_path(self, *join_paths):
        return os.path.join(self._base_path, *join_paths)

    def overlays_path(self, *join_paths):
        return self.service_path(constants.OVERLAYS_DIR, *join_paths)


class ManagedAppContainer(object):
    """A wrapper for AppContainer.

    It provides an interface to AppContainer that is aware of the service
    """
    def __init__(self, service, container):
        self._service = service
        self._container = container

    def destroy(self):
        self._container.destroy()

    def start(self):
        return self._container.start()

    def stop(self):
        return self._container.stop()

    @property
    def name(self):
        return self._container.name

    def make_image(self, name=None, image_writer=None):
        # Setup defaults from args
        name = name or self._image_name()
        image_writer = image_writer or AppContainerImageWriter.new()

        # Setup file_path
        filename = '%s.%s' % (name, constants.IMAGE_FILE_EXTENSION)
        file_path = self._service.service_path(
                constants.CONTAINER_IMAGES_LIB_DIR, filename)
        self._container.make_image(file_path, image_writer)
        return file_path

    def _image_name(self):
        name = self._container.name
        timestamp = time.time()
        return "%s-%s" % (name, timestamp)
