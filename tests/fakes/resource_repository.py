import ipaddr


class FakeAppContainerMetadata(object):
    @classmethod
    def create(cls, name, ip, mac, base):
        ip = ipaddr.IPv4Address(ip)
        return cls(name, ip, mac, base)

    def __init__(self, name, ip, mac, base):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.base = base


class FakeAppContainerMetadataRepository(object):
    """A fake implementation of the ResourceRepository

    It uses a dictionary to store the data.
    """
    def __init__(self, *args, **kwargs):
        self._resources = dict()

    def _setup_resources(self, metadatas):
        """Sets up fake ResourceReservations"""
        resources = self._resources
        for metadata_tuple in metadatas:
            resources[metadata_tuple[0]] = FakeResourceReservation.create(
                    *metadata_tuple)

    def all(self):
        """Returns a sorted list of all resources"""
        return sorted(self._resources.values(), key=lambda a: a.name)

    def save(self, metadata):
        """Fake saves a metadata"""
        pass
