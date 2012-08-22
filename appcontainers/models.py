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
    def create(cls, lxc, metadata):
        """Creates a new app container

        :param lxc: This app container's associated LXC
        :type lxc: LXC
        :param metadata: this AppContainer's AppContainerMetadata
        :type metadata: AppContainerMetadata
        """
        return cls(lxc, metadata)

    def __init__(self, lxc, metadata):
        self.lxc = lxc
        self._metadata = metadata

    @property
    def name(self):
        return self._metadata.name

    @property
    def base(self):
        return self._metadata.base

    @property
    def image(self):
        return self._metadata.image

    def start(self):
        self.lxc.start()

    def stop(self):
        self.lxc.stop()

    def destroy(self):
        # Destroy LXC
        self.lxc.destroy()

    def __repr__(self):
        return '<AppContainer [%s]>' % self.name


class AppContainerMetadata(object):
    @classmethod
    def create(cls, name, ip, mac, base, image=None):
        return cls(name, ip, mac, base, image)

    def __init__(self, name, ip, mac, base, image):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.base = base
        self.image = image

    def __repr__(self):
        return '<AppContainerMetadata [%s, %s, %s]>' % (self.name,
                self.ip, self.mac)


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
