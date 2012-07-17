"""
appcontainer.api
~~~~~~~~~~~~~~~~

The appcontainers API
"""
from . import constants
from .service import AppContainerService
from .resources import setup_resource_service
from .creator import setup_app_container_creator
from .settings import Settings
        
import os

class LXC(object):

    local_test = os.path.abspath('localer')
    def path(self, *join_paths):
        return os.path.join(self.local_test, *join_paths)



class lxc4u(object):
    @classmethod
    def create(cls, *args, **kwargs):
        print "NOT ACTUALLY CREATING AN LXC"
        return LXC()

def setup_service():
    """Creates an AppContainerService based on the settings"""
    settings = _create_settings()
    resource_repository = _create_resource_repository()
    resource_service = setup_resource_service(settings, resource_repository)
    app_container_creator = setup_app_container_creator(settings, lxc4u)
    return AppContainerService(resource_service, app_container_creator)

def _create_settings(**kwargs):
    import ipaddr
    settings = Settings(base_path='/var/lib/appcontainers', 
            network=ipaddr.IPv4Network('192.168.0.0/24'),
            mac_range=['00:16:3e:00:00:00', '00:16:3e:00:01:00'])
    return settings

def _create_resource_repository():
    """Creates a resource repository"""
    from tests.fakes import FakeResourceReservationRepository
    resource_repository = FakeResourceReservationRepository()
    resource_repository._setup_resources([
        ('alpha', '192.168.0.1', '00:16:3e:00:00:00'),
        ('bravo', '192.168.0.2', '00:16:3e:00:00:01'),
        ('charlie', '192.168.0.3', '00:16:3e:00:00:02'),
    ])
    return resource_repository

def _wire_dependencies():
    """Wires the dependencies for the AppContainerService"""
    pass
