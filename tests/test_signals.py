from mock import Mock, patch
from appcontainers.signals import *


def test_initialize_a_signal():
    signal = Signal.create('sig')
    assert signal.name == 'sig'


class ClassWithSignals(SignalsMixin):
    """A class for testing the signals mixin"""
    pass


@patch('appcontainers.signals.Signal')
def test_publish_signal(mock_signal_cls):
    mock_function = Mock()
    obj = ClassWithSignals()
    obj.bind_to_signal('signal', mock_function)
    obj.publish_signal('signal', 'a', 'b', test='hello')

    mock_function.assert_called_with(mock_signal_cls.create.return_value,
            obj, 'a', 'b', test='hello')
