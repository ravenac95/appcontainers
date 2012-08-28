from mock import Mock
from appcontainers import constants
from appcontainers.service import *


class TestAppContainerService(object):
    def setup(self):
        mock_container_service = Mock()
        mock_creator = Mock()
        mock_session = Mock()
        mock_database = Mock()
        mock_loader = Mock()
        mock_container_repository = Mock()
        self.service = AppContainerService(
                app_container_metadata_service=mock_container_service,
                creator=mock_creator,
                loader=mock_loader,
                session=mock_session,
                database=mock_database,
                app_container_metadata_repository=mock_container_repository,
                base_path='/var/lib/appcontainers'
                )
        self.mock_container_service = mock_container_service
        self.mock_creator = mock_creator
        self.mock_session = mock_session
        self.mock_database = mock_database

    def test_provision(self):
        # Run Test
        base = 'abase'
        image = None
        self.service.provision(base=base)

        # Assertions
        self.mock_container_service.provision_metadata.assert_called_with(base,
                image)
        self.mock_creator.provision_container.assert_called_with(
                self.mock_container_service.provision_metadata.return_value)
        self.mock_session.commit.assert_called_with()

    def test_service_path(self):
        assert self.service.service_path('hello') == (
            '/var/lib/appcontainers/hello'
        )

    def test_overlay_path(self):
        expected = '/var/lib/appcontainers/%s/hello' % constants.OVERLAYS_DIR
        assert self.service.overlays_path('hello') == expected

    def test_close(self):
        self.service.close()

        self.mock_session.abort.assert_called_with()
        self.mock_database.close.assert_called_with()
