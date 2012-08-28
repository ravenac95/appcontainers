from nose.tools import eq_
from nose.plugins.attrib import attr
from appcontainers.service import *
import appcontainers
from .utils import only_as_root


@attr('large')
class TestAppContainersAPI(object):
    @only_as_root
    def setup(self):
        self.service = appcontainers.setup_service()

    @only_as_root
    def teardown(self):
        self.service.close()

    @only_as_root
    def test_provision_a_container(self):
        service = self.service
        destroyed = False
        try:
            container = service.provision()
            # Grab the contained LXC as a fail-safe
            lxc = container._container.lxc
            assert isinstance(container, ManagedAppContainer) == True

            container.destroy()
            destroyed = True
        finally:
            if not destroyed:
                try:
                    lxc.destroy()
                except:
                    pass

    @only_as_root
    def test_provision_start_and_stop_many_containers(self):
        service = self.service
        containers_before = service.list_containers()
        containers = []
        count = 10

        try:
            for i in xrange(count):
                container = service.provision()
                containers.append(container)
                container.start()
                container.stop()
        finally:
            for container in containers:
                container.destroy()

        containers_after = service.list_containers()
        eq_(containers_before, containers_after)
