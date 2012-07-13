import uuid
import ipaddr


class ResourcesUnavailable(Exception):
    pass


class Unavailable(Exception):
    pass


class ResourceService(object):
    def __init__(self, repository, settings, reservation_cls=None):
        self._repository = repository
        self._settings = settings
        self._reservation_cls = reservation_cls

    def make_reservation(self):
        reservations = self._repository.all()
        # Arrays to track each used resource
        names = []
        ips = []
        macs = []
        # Collect used resources
        for reservation in reservations:
            names.append(reservation.name)
            ips.append(reservation.ip)
            macs.append(reservation.mac)
        # Generate available resources
        name = available_name(names)
        ip = available_ip(ips, self._settings.network)
        mac = available_mac(macs, self._settings.mac_range)

        reservation = self.reservation_cls.create(name, ip, mac)
        self._repository.save(reservation)
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
        raise Unavailable('No IP Address available in network: %s' % network)
    return found_ip


def available_mac(used_macs, mac_range):
    mac_int_range = map(mac_str_to_int, mac_range)

    found_mac = None
    for mac in xrange(*mac_int_range):
        mac_str = mac_int_to_str(mac)
        if not mac_str in used_macs:
            found_mac = mac_str
            break
    if not found_mac:
        range_str = ' - '.join(mac_range)
        raise Unavailable('No Mac Address available in range: %s' % range_str)
    return found_mac


def mac_str_to_int(mac_str):
    mac_str = mac_str.replace(':', '')
    mac_int = int(mac_str, 16)
    return mac_int


def mac_int_to_str(mac_int):
    mac_str = hex(mac_int)
    mac_str = mac_str[2:]

    leading_str = '0' * (12 - len(mac_str))
    mac_str = '%s%s' % (leading_str, mac_str)

    split_str = [mac_str[i:i+2] for i in range(0, len(mac_str), 2)]
    return ':'.join(split_str)
