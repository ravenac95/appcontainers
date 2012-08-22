"""
appcontainer.api
~~~~~~~~~~~~~~~~

The appcontainers API
"""
import lxc4u
from .service import AppContainerService
from .creator import setup_app_container_creator
from .loader import setup_app_container_loader
from .settings import Settings
from .database import LocalDatabase, Session
from .metadata import AppContainerMetadataRepository, setup_metadata_service
from .resources import ResourceReservationRepository


def setup_service():
    """Creates an AppContainerService based on the settings"""
    lxc_service = lxc4u

    settings = _create_settings()

    database = LocalDatabase.connect(settings.database_path())

    session = Session()

    metadata_repository = _create_app_container_metadata_repository(database)

    metadata_service = setup_metadata_service(settings, metadata_repository)

    app_container_creator = setup_app_container_creator(settings, lxc_service)

    app_container_loader = setup_app_container_loader(settings, lxc_service)

    return AppContainerService(metadata_service, app_container_creator,
            app_container_loader, session, database, metadata_repository)


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


def _create_app_container_metadata_repository(database):
    """Creates a resource repository"""
    metadata_repository = AppContainerMetadataRepository(database)
    return metadata_repository


def _wire_dependencies():
    """Wires the dependencies for the AppContainerService"""
    pass
