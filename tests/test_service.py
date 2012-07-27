from mock import Mock
from appcontainers import constants
from appcontainers.service import *


class TestAppContainerService(object):
    def setup(self):
        mock_resource_service = Mock()
        mock_creator = Mock()
        mock_session = Mock()
        mock_database = Mock()
        mock_resource_repository = Mock()
        self.service = AppContainerService(
                resource_service=mock_resource_service,
                session=mock_session,
                database=mock_database,
                resource_repository=mock_resource_repository,
                creator=mock_creator)
        self.mock_resource_service = mock_resource_service
        self.mock_creator = mock_creator
        self.mock_session = mock_session

    def test_service_provision(self):
        # Run Test
        base = 'abase'
        self.service.provision(base=base)

        # Assertions
        self.mock_resource_service.make_reservation.assert_called_with()
        self.mock_creator.provision_container.assert_called_with(base,
                self.mock_resource_service.make_reservation.return_value)
        self.mock_session.commit.assert_called_with()

    def test_service_service_path(self):
        assert self.service.service_path('hello') == (
            '/var/lib/appcontainers/hello'
        )

    def test_service_overlay_path(self):
        expected = '/var/lib/appcontainers/%s/hello' % constants.OVERLAYS_DIR
        assert self.service.overlays_path('hello') == expected
