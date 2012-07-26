from .signals import SignalsMixin


class AppContainer(SignalsMixin):
    @classmethod
    def create(cls, base, lxc, reservation, directory_list):
        """Creates a new app container

        :param base: identifier for the base
        :type base: str
        :param lxc: This app container's associated LXC
        :type lxc: LXC
        :param reservation: this AppContainer's ResourceReservation
        :type reservation: ResourceReservation
        :param directory_list: A DirectoryList that manages this container's
            directories
        :type directory_list: DirectoryList
        """
        return cls(base, lxc, reservation, directory_list)

    def __init__(self, base, lxc, reservation, directory_list):
        self._base = base
        self.lxc = lxc
        self._reservation = reservation
        self._directory_list = directory_list

    @property
    def name(self):
        return self._reservation.name

    def start(self):
        self.lxc.start()

    def stop(self):
        self.lxc.stop()

    def destroy(self):
        # Destroy LXC
        self.lxc.destroy()

        # Destroy AppContainer's directories
        self._directory_list.destroy()

        # Fire destroy event
        self.publish_signal('destroyed')

    def make_image(self, path, writer):
        writer.create(path, self._base, self._directory_list[-1])


class ResourceReservation(object):
    @classmethod
    def create(cls, name, ip, mac):
        return cls(name, ip, mac)

    def __init__(self, name, ip, mac):
        self.name = name
        self.ip = ip
        self.mac = mac

    def __repr__(self):
        return "<ResourceReservation [%s, %s, %s]>" % (self.name,
                self.ip, self.mac)
