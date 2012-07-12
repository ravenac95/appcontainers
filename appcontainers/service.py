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
    """The gateway to using app containers"""
    def __init__(self, base_path='/var/lib/appcontainers'):
        self._base_path = base_path

    def provision(self, base='base'):
        """Provision a new app container using the default base"""
        # Setup the information for the container
        builder = AppContainerBuilder()
        options = dict(name=self._random_name())
        network = self._reserve_network_resources()
        options['network'] = network
        return builder.provision_container(options)

    def service_path(self, *join_paths):
        return os.path.join(self._base_path, *join_paths)

    def overlays_path(self, *join_paths):
        return self.service_path(constants.OVERLAYS_DIR, *join_paths)

    def _reserve_network_resources(self):
        """Reserves an ip address for a new app container"""
        # Compile the reserved resources
        reservations = self.service_state.resource_reservations()
        ips = [] 
        macs = []
        # Use the lowest available mac and ip
        for name, reservation in reservations.iteritems():
            ips.append(reservation['ip'])
            macs.append(reservation['mac'])
        # return the ip address

class AppContainerBuilder(object):
    def provision_container(self, options):
        return options

