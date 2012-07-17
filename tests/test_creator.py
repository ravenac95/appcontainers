from mock import Mock
from appcontainers.creator import *
from tests.fakes import *


class TestAppContainerCreator(object):
    def setup(self):
        mock_settings = Mock()
        mock_app_container_cls = Mock()
        mock_lxc_service = Mock()
        mock_skeleton_assembler = Mock()

        creator = AppContainerCreator(mock_settings,
                app_container_cls=mock_app_container_cls,
                lxc_service=mock_lxc_service,
                skeleton_assembler=mock_skeleton_assembler)
        self.creator = creator

        self.mock_settings = mock_settings
        self.mock_app_container_cls = mock_app_container_cls
        self.mock_lxc_service = mock_lxc_service
        self.mock_skeleton_assembler = mock_skeleton_assembler

    def test_app_container_creator_provision_container(self):
        fake_reservation = FakeResourceReservation.create('somename',
                '192.168.0.1', '00:16:3e:00:00:00')
        container = self.creator.provision_container('base', fake_reservation)
        # Mock Assertions
        self.mock_skeleton_assembler.setup.assert_called_with(
                self.mock_settings,
                self.mock_lxc_service.create.return_value,
                fake_reservation)

        # Assert return value
        assert container == self.mock_app_container_cls.create.return_value
