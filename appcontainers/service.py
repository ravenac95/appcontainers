import os
import shutil
import time
from . import constants


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
    def __init__(self,
            app_container_metadata_service,
            creator,
            loader,
            session,
            database,
            app_container_metadata_repository,
            base_path='/var/lib/appcontainers'):
        self._base_path = base_path
        self._creator = creator
        self._loader = loader
        self._session = session
        self._metadata_service = app_container_metadata_service
        self._metadata_repository = app_container_metadata_repository
        self._database = database

    def provision(self, base='base'):
        """Provision a new app container using the default base"""
        # Setup the information for the container
        app_container_metadata = self._metadata_service.provision_metadata(
                base, None)
        app_container = self._creator.provision_container(
                app_container_metadata)
        self._session.commit()
        return ManagedAppContainer(self, app_container)

    def service_path(self, *join_paths):
        return os.path.join(self._base_path, *join_paths)

    def overlays_path(self, *join_paths):
        return self.service_path(constants.OVERLAYS_DIR, *join_paths)

    def images_path(self, *join_paths):
        return self.service_path(constants.IMAGES_DIR, *join_paths)

    def destroy(self, container):
        # Destroy container
        container.destroy()

        # Delete the overlay directories
        shutil.rmtree(self.overlays_path(container.name))

        # Delete the metadata
        self._metadata_repository.delete(container._metadata)
        self._session.commit()

    @property
    def database(self):
        return self._database

    def make_image(self, container, image_name, image_writer=None):
        image_filename = "%s.%s" % (image_name, constants.IMAGE_FILE_EXTENSION)
        image_path = self.images_path('lib', image_filename)
        container.make_image(image_path, image_name=image_name,
                image_writer=image_writer)
        return image_path

    def list_containers(self):
        metadatas = self._metadata_repository.all()
        app_containers = map(self._loader.load_container, metadatas)
        return map(lambda a: ManagedAppContainer(self, a), app_containers)


class ManagedAppContainer(object):
    """A wrapper for AppContainer.

    It provides an interface to AppContainer that is aware of the service
    """
    def __init__(self, service, container):
        self._service = service
        self._container = container

    def __repr__(self):
        return '<ManagedAppContainer %s>' % self.name

    def destroy(self):
        self._service.destroy(self._container)

    def start(self):
        return self._container.start()

    def stop(self):
        return self._container.stop()

    @property
    def name(self):
        return self._container.name

    @property
    def ip(self):
        return self._container.ip

    @property
    def mac(self):
        return self._container.mac

    def make_image(self, image_name=None, image_writer=None):
        # Setup defaults from args
        image_name = image_name or self._image_name()
        # Setup file_path
        self._service.make_image(self._container, image_name,
                image_writer=image_writer)

    def _image_name(self):
        name = self._container.name
        timestamp = int(time.time())
        return "%s-%s" % (name, timestamp)
