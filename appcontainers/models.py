class AppContainer(object):
    @classmethod
    def create(cls, base, lxc, reservation):
        return cls(base, lxc, reservation)

    def __init__(self, base, lxc, reservation):
        self.base = base
        self.lxc = lxc
        self.reservation = reservation
    
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
