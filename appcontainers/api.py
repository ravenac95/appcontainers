"""
appcontainer.api
~~~~~~~~~~~~~~~~

The appcontainers API
"""
import lxc4u
from .service import AppContainerService
from .resources import setup_resource_service
from .creator import setup_app_container_creator
from .settings import Settings
from .database import LocalDatabase, Session
from .resources import ResourceReservationRepository


def setup_service():
    """Creates an AppContainerService based on the settings"""
    settings = _create_settings()

    database = LocalDatabase.connect(settings.database_path())

    session = Session()

    resource_repository = _create_resource_repository(database)

    resource_service = setup_resource_service(settings, resource_repository)

    app_container_creator = setup_app_container_creator(settings, lxc4u)

    return AppContainerService(resource_service, app_container_creator,
            session, database, resource_repository)


def _create_settings(**kwargs):
    # FIXME FAKED
    import ipaddr
    settings = Settings(base_path='/var/lib/appcontainers',
            network=ipaddr.IPv4Network('192.168.0.0/24'),
            mac_range=['02:16:3e:00:00:00', '02:16:3e:00:01:00'])
    return settings


def _create_fake_resource_repository(database):
    """Creates a resource repository"""
    # FIXME FAKED
    from tests.fakes import FakeResourceReservationRepository
    resource_repository = FakeResourceReservationRepository()
    resource_repository._setup_resources([
        ('alpha', '192.168.0.1', '00:16:3e:00:00:00'),
        ('bravo', '192.168.0.2', '00:16:3e:00:00:01'),
        ('charlie', '192.168.0.3', '00:16:3e:00:00:02'),
    ])
    return resource_repository


def _create_resource_repository(database):
    """Creates a resource repository"""
    resource_repository = ResourceReservationRepository(database)
    return resource_repository


def _wire_dependencies():
    """Wires the dependencies for the AppContainerService"""
    pass
