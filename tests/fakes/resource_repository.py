import ipaddr

class FakeResourceReservation(object):
    @classmethod
    def create(cls, name, ip, mac):
        ip = ipaddr.IPv4Address(ip)
        return cls(name, ip, mac)

    def __init__(self, name, ip, mac):
        self.name = name
        self.ip = ip
        self.mac = mac

class FakeResourceReservationRepository(object):
    """A fake implementation of the ResourceRepository 
    
    It uses a dictionary to store the data.
    """
    def __init__(self, *args, **kwargs):
        self._resources = dict()

    def _setup_resources(self, reservations):
        """Sets up fake ResourceReservations"""
        resources = self._resources
        for reservation_tuple in reservations:
            resources[reservation_tuple[0]] = FakeResourceReservation.create(
                    *reservation_tuple)

    def all(self):
        """Returns a sorted list of all resources"""
        return sorted(self._resources.values(), key=lambda a: a.name)

    def save(self, reservation):
        """Fake saves a reservation"""
        pass
