import os
import constants

def create_app_container_object():
    return None

# Process for creating an app container
#
# Provision container with overlays
# Add files to container
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
        return self._creator.provision_container(resource_reservation)

    def service_path(self, *join_paths):
        return os.path.join(self._base_path, *join_paths)

    def overlays_path(self, *join_paths):
        return self.service_path(constants.OVERLAYS_DIR, *join_paths)

