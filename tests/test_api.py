from nose.plugins.attrib import attr
from appcontainers.models import *
import appcontainers
from .utils import only_as_root


@attr('large')
class TestAppContainersAPI(object):
    @only_as_root
    def test_provision_a_container(self):
        service = appcontainers.setup_service()
        try:
            container = service.provision()
            lxc = container.lxc
            assert isinstance(container, AppContainer) == True

            container.destroy()
        finally:
            try:
                lxc.destroy()
            except:
                pass
