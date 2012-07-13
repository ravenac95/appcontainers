from mock import Mock
from appcontainers import constants 
from appcontainers.service import *

class TestAppContainerService(object):
    def setup(self):
        resource_service = Mock()
        creator = Mock()
        self.service = AppContainerService(
                resource_service=resource_service,
                creator=creator)
        self.mock_resource_service = resource_service
        self.mock_creator = creator

    def test_service_provision(self):
        # Run Test
        self.service.provision()
        
        # Assertions
        self.mock_resource_service.make_reservation.assert_called_with()
        self.mock_creator.provision_container.assert_called_with(
                self.mock_resource_service.make_reservation.return_value)

    def test_service_service_path(self):
        assert self.service.service_path('hello') == '/var/lib/appcontainers/hello'

    def test_service_overlay_path(self):
        expected = '/var/lib/appcontainers/%s/hello' % constants.OVERLAYS_DIR
        assert self.service.overlays_path('hello') == expected
