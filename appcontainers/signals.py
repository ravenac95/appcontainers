class Signal(object):
    @classmethod
    def create(cls, name):
        return cls(name)

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


class SignalsMixin(object):
    """A mixin for signal publishers

    This allows for signals very similar to javascript.
    """
    def publish_signal(self, signal_name, *data, **kwargs):
        """Publishes signals"""
        signal_to_publish = Signal.create(signal_name)
        listeners = self._listeners
        for listener in listeners:
            listener(signal_to_publish, self, *data, **kwargs)

    @property
    def _listeners(self):
        """A property that always returns a list of listeners"""
        attr_name = '_signals_mixin_listeners'
        listeners = getattr(self, attr_name, None)
        if not listeners:
            listeners = []
            setattr(self, attr_name, listeners)
        return listeners

    def bind_to_signal(self, signal_name, callback):
        """Allows subscribers to directly listen to signals on this object"""
        listeners = self._listeners
        listeners.append(callback)
