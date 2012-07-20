from mock import Mock, ANY
from appcontainers.models import *


def test_initialize_app_container():
    container = AppContainer.create(None, None, None, None)
    assert isinstance(container, AppContainer) == True


class TestAppContainer(object):
    def setup(self):
        self.mock_lxc = Mock()
        self.mock_reservation = Mock()
        self.mock_directory_list = Mock()
        self.container = AppContainer.create('base', self.mock_lxc,
                self.mock_reservation, self.mock_directory_list)

    def test_start(self):
        self.container.start()

        self.mock_lxc.start.assert_called_with()

    def test_stop(self):
        self.container.stop()

        self.mock_lxc.stop.assert_called_with()

    def test_destroy(self):
        self.container.destroy()

        self.mock_lxc.destroy.assert_called_with()
        self.mock_directory_list.destroy.assert_called_with()

    def test_destroy_with_signal(self):
        mock_listener = Mock()

        self.container.bind_to_signal('destroyed', mock_listener)
        self.container.destroy()

        mock_listener.assert_called_with(ANY, self.container)
