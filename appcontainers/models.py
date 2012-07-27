class AncestorInfo(object):
    """An object used to describe an app container's ancestry"""
    @classmethod
    def create(cls, base, image=None):
        return cls(base, image)

    def __init__(self, base, image):
        self._base = base
        self._image = image

    @property
    def base(self):
        return self._base

    @property
    def image(self):
        return self._image


class AppContainer(object):
    @classmethod
    def create(cls, ancestor_info, lxc, reservation):
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
        return cls(ancestor_info, lxc, reservation)

    def __init__(self, ancestor_info, lxc, reservation):
        self._ancestor_info = ancestor_info
        self.lxc = lxc
        self._reservation = reservation

    @property
    def name(self):
        return self._reservation.name

    @property
    def ancestor_info(self):
        return self._ancestor_info

    def start(self):
        self.lxc.start()

    def stop(self):
        self.lxc.stop()

    def destroy(self):
        # Destroy LXC
        self.lxc.destroy()

    def __repr__(self):
        return '<AppContainer [%s]>' % self.name


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
