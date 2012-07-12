import mock
from appcontainers import constants 
from appcontainers.service import *

def test_initialize_service():
    service = AppContainerService()

class FakeAppContainerService(AppContainerService):
    reservations = dict(ip='0.0.0.0', mac='00:00:00:00:00:00')
    random_name = 'somename'

    def _reserve_network_resources(self):
        return self.reservations

    def _random_name(self):
        return self.random_name

class TestAppContainerService(object):
    def setup(self):
        self.service = FakeAppContainerService()

    @mock.patch('appcontainers.service.AppContainerBuilder')
    def test_service_provision(self, builder):
        FakeService = FakeAppContainerService
        options = dict(name=FakeService.random_name)
        options['network'] = FakeAppContainerService.reservations

        self.service.provision()
        builder.return_value.provision_container.assert_called_with(options)

    def test_service_service_path(self):
        assert self.service.service_path('hello') == '/var/lib/appcontainers/hello'

    def test_service_overlay_path(self):
        expected = '/var/lib/appcontainers/%s/hello' % constants.OVERLAYS_DIR
        assert self.service.overlays_path('hello') == expected

