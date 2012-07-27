from mock import Mock, MagicMock, ANY
from appcontainers.models import *


def test_initialize_app_container():
    container = AppContainer.create(None, None, None)
    assert isinstance(container, AppContainer) == True


class TestAppContainer(object):
    def setup(self):
        self.mock_ancestor_info = Mock()
        self.mock_lxc = Mock()
        self.mock_reservation = Mock()
        self.container = AppContainer.create(self.mock_ancestor_info,
                self.mock_lxc, self.mock_reservation)

    def test_start(self):
        self.container.start()

        self.mock_lxc.start.assert_called_with()

    def test_stop(self):
        self.container.stop()

        self.mock_lxc.stop.assert_called_with()

    def test_destroy(self):
        self.container.destroy()

        self.mock_lxc.destroy.assert_called_with()
