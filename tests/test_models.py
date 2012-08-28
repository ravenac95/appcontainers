from mock import Mock, MagicMock
from appcontainers.models import *


def test_initialize_app_container():
    container = AppContainer.create(None, None)
    assert isinstance(container, AppContainer) == True


class TestAppContainer(object):
    def setup(self):
        self.mock_ancestor_info = Mock()
        self.mock_lxc = Mock()
        self.mock_metadata = Mock()
        self.container = AppContainer.create(self.mock_lxc, self.mock_metadata)

    def test_start(self):
        self.mock_lxc.status = 'RUNNING'
        self.container.start()

        self.mock_lxc.start.assert_called_with()

    def test_stop(self):
        self.mock_lxc.status = 'STOPPED'
        self.container.stop()

        self.mock_lxc.stop.assert_called_with()

    def test_destroy(self):
        self.container.destroy()

        self.mock_lxc.destroy.assert_called_with()
