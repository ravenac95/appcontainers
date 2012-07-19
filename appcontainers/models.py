
class DirectoryManager():
    pass


class AppContainer(object):
    @classmethod
    def create(cls, base, lxc, reservation, directories):
        directory_manager = DirectoryManager.new(directories)
        return cls(base, lxc, reservation)

    def __init__(self, base, lxc, reservation, directory_manager):
        self._base = base
        self.lxc = lxc
        self._reservation = reservation
        self._directories = directories

    def start(self):
        self.lxc.start()

    def stop(self):
        self.lxc.stop()

    def destroy(self):
        # Destroy LXC
        self.lxc.destroy()

        # Destroy AppContainer's storage


class ResourceReservation(object):
    @classmethod
    def create(cls, name, ip, mac):
        return cls(name, ip, mac)

    def __init__(self, name, ip, mac):
        self.name = name
        self.ip = ip
        self.mac = mac

    def __repr__(self):
        return "<ResourceReservation [%s, %s, %s]>" % (self.name, self.ip,
                self.mac)
