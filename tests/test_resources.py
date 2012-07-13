import ipaddr
from nose.tools import raises
from mock import Mock, patch, ANY
from appcontainers.resources import *
from tests.fakes.resource_repository import *


class TestResourceService(object):
    def setup(self):
        settings = Mock()
        reservation_cls = Mock()
        resource_repository = FakeResourceReservationRepository()
        resource_repository._setup_resources([
            ('a', 'ip_a', 'mac_a'),
            ('b', 'ip_b', 'mac_b'),
            ('c', 'ip_c', 'mac_c'),
        ])

        self.service = ResourceService(resource_repository, settings,
                reservation_cls=reservation_cls)

        self.mock_settings = settings
        self.mock_reservation_cls = reservation_cls
        self.mock_repository = resource_repository

    @patch('appcontainers.resources.available_name', autospec=True)
    @patch('appcontainers.resources.available_ip', autospec=True)
    @patch('appcontainers.resources.available_mac', autospec=True)
    def test_make_reservation(self, mock_mac, mock_ip, mock_name):
        # Run test
        reservation = self.service.make_reservation()

        # Assertions
        mock_name.assert_called_with(['a', 'b', 'c'])
        mock_ip.assert_called_with(['ip_a', 'ip_b', 'ip_c'], ANY)
        mock_mac.assert_called_with(['mac_a', 'mac_b', 'mac_c'])
   
        self.mock_reservation_cls.create.assert_called_with(
                mock_name.return_value, mock_ip.return_value, 
                mock_mac.return_value)
        assert reservation == self.mock_reservation_cls.create.return_value

def test_available_name():
    # FIXME this isn't a good test. It might fail sometimes
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
def test_available_ips_none():
    network = ipaddr.IPv4Network('192.168.0.0/32')
    used = []
    available_ip(used, network)

def test_available_mac():
    used = ['00:16:3e:00:00:00',
            '00:16:3e:00:00:02',
            '00:16:3e:00:00:03',
            ]
    mac = available_mac(used)
    assert mac == '00:16:3e:00:00:04'
