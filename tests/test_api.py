from nose.plugins.attrib import attr
from appcontainers.service import *
import appcontainers
from .utils import only_as_root


@attr('large')
class TestAppContainersAPI(object):
    @only_as_root
    def test_provision_a_container(self):
        service = appcontainers.setup_service()
        destroyed = False
        try:
            container = service.provision()
            # Grab the contained LXC as a fail-safe
            lxc = container._container.lxc
            assert isinstance(container, ManagedAppContainer) == True

            container.destroy()
            destroyed = True
        finally:
            if destroyed:
                try:
                    lxc.destroy()
                except:
                    pass
