import uuid
import ipaddr

class ResourcesUnavailable(Exception):
    pass

class Unavailable(Exception):
    pass

class ResourceService(object):
    def __init__(self, repository, settings, reservation_cls=None):
        self.repository = repository
        self.settings = settings
        self.reservation_cls = reservation_cls

    def make_reservation(self):
        reservations = self.repository.all()

        names = []
        ips = []
        macs = []

        for reservation in reservations:
            names.append(reservation.name)
            ips.append(reservation.ip)
            macs.append(reservation.mac)

        name = available_name(names)
        ip = available_ip(ips, self.settings.network)
        mac = available_mac(macs)

        reservation = self.reservation_cls.create(name, ip, mac)
        return reservation

def available_name(used_names):
    while True:
        name = uuid.uuid4().hex
        if not name in used_names:
            break
    return name

def available_ip(used_ips, network):
    """Find the first available ip address"""
    network = ipaddr.IPv4Network(network)
    found_ip = None
    for ip in network.iterhosts():
        if not ip in used_ips:
            found_ip = ip
            break
    if not found_ip:
        raise Unavailable('No IP Address available in %s' % network)
    return found_ip

def available_mac():
    pass

