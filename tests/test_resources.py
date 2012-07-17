import ipaddr
from nose.plugins.attrib import attr
from nose.tools import raises
from mock import Mock, patch, ANY
from appcontainers.resources import *
from tests.fakes import *

TEST_NAMES = ['a', 'b', 'c']
TEST_IPS = map(ipaddr.IPv4Address, ['192.168.0.1', '192.168.0.2', '192.168.0.3'])
TEST_MACS = ['00:16:3e:00:00:00', '00:16:3e:00:00:01', 
        '00:16:3e:00:00:02']

def fake_resource_reservation_repository_setup(resources=None):
    default_resources = zip(TEST_NAMES, TEST_IPS, TEST_MACS)
    resource_repository = FakeResourceReservationRepository()
    resource_repository._setup_resources(default_resources)
    return resource_repository


class TestResourceService(object):
    def setup(self):
        settings = Mock()
        reservation_cls = Mock()
        resource_repository = fake_resource_reservation_repository_setup()

        self.service = ResourceService(settings, resource_repository,
                reservation_cls=reservation_cls)

        self.mock_settings = settings
        self.mock_reservation_cls = reservation_cls
        self.mock_repository = resource_repository

    @patch('appcontainers.resources.available_name', autospec=True)
    @patch('appcontainers.resources.available_ip', autospec=True)
    @patch('appcontainers.resources.available_mac', autospec=True)
    def test_make_reservation(self, mock_mac, mock_ip, mock_name):
        # Inspect the save method
        mock_save = Mock()
        self.mock_repository.save = mock_save

        # Run test
        reservation = self.service.make_reservation()

        # Assertions
        mock_name.assert_called_with(TEST_NAMES)
        mock_ip.assert_called_with(TEST_IPS, ANY)
        mock_mac.assert_called_with(TEST_MACS, ANY)

        self.mock_reservation_cls.create.assert_called_with(
                mock_name.return_value, mock_ip.return_value,
                mock_mac.return_value)
        created_reservation = self.mock_reservation_cls.create.return_value
        mock_save.assert_called_with(created_reservation)
        assert reservation == created_reservation


def test_available_name():
    # FIXME this isn't a good test. It doesn't really tell us anything
    used = ['a', 'b', 'c']
    name = available_name(used)
    assert not name in used


def test_available_ips():
    used1 = [ipaddr.IPv4Address('192.168.0.1'),
            ipaddr.IPv4Address('192.168.0.3')]
    used2 = [ipaddr.IPv4Address('192.168.0.1'),
            ipaddr.IPv4Address('192.168.0.2'),
            ipaddr.IPv4Address('192.168.0.3')]
    network_object = ipaddr.IPv4Network('192.168.0.0/24')
    network_as_string = '192.168.0.0/24'

    ip1 = available_ip(used1, network_object)
    ip2 = available_ip(used2, network_as_string)
    assert ip1 == ipaddr.IPv4Address('192.168.0.2')
    assert ip2 == ipaddr.IPv4Address('192.168.0.4')


@raises(Unavailable)
def test_available_ips_fails():
    network = ipaddr.IPv4Network('192.168.0.0/32')
    used = []
    available_ip(used, network)


def test_available_mac():
    used1 = [
        '00:16:3e:00:00:00',
        '00:16:3e:00:00:01',
        '00:16:3e:00:00:02',
        '00:16:3e:00:00:03',
    ]
    used2 = [
        '00:16:3e:00:00:00',
        '00:16:3e:00:00:01',
        '00:16:3e:00:00:03',
        '00:16:3e:00:00:04',
    ]
    mac_range = ['00:16:3e:00:00:00', '00:16:3e:00:00:ff']
    mac1 = available_mac(used1, mac_range)
    mac2 = available_mac(used2, mac_range)

    assert mac1 == '00:16:3e:00:00:04'
    assert mac2 == '00:16:3e:00:00:02'


@raises(Unavailable)
def test_available_mac_fails():
    mac_range = ['00:16:3e:00:00:00', '00:16:3e:00:00:00']
    used = []
    available_mac(used, mac_range)


def test_mac_str_to_int():
    tests = [
        ('00:16:3e:00:00:00', 95529467904),
        ('00:16:3e:00:ff:00', 95529533184),
        ('00:00:00:00:00:00', 0),
        ('ff:ff:ff:ff:ff:ff', 281474976710655),
    ]
    for test, expected in tests:
        yield do_mac_str_to_int, test, expected


def do_mac_str_to_int(test, expected):
    assert mac_str_to_int(test) == expected


def test_mac_int_to_str():
    tests = [
        (95529467904, '00:16:3e:00:00:00'),
        (95529533184, '00:16:3e:00:ff:00'),
        (0, '00:00:00:00:00:00'),
        (281474976710655, 'ff:ff:ff:ff:ff:ff'),
    ]
    for test, expected in tests:
        yield do_mac_int_to_str, test, expected


def do_mac_int_to_str(test, expected):
    assert mac_int_to_str(test) == expected


@attr('medium')
def test_resource_service_making_resources():
    """Test the resource service with the available_* functions"""
    # Use the default setup from the beginning of the file
    resource_repository = fake_resource_reservation_repository_setup()
    reservation_cls = FakeResourceReservation
    settings = FakeSettings(network=ipaddr.IPv4Network('192.168.0.0/24'),
            mac_range=['00:16:3e:00:00:00', '00:16:3e:00:01:00'])

    service = ResourceService(settings, resource_repository,
            reservation_cls=reservation_cls)

    reservation = service.make_reservation()

    assert reservation.name is not None
    assert reservation.ip == ipaddr.IPv4Address('192.168.0.4')
    assert reservation.mac == '00:16:3e:00:00:03'
