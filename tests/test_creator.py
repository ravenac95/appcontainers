from mock import Mock, patch, create_autospec
from appcontainers.creator import *
from tests.fakes import *


class TestAppContainerCreator(object):
    def setup(self):
        from appcontainers.models import AppContainer, AncestorInfo
        mock_settings = Mock()
        mock_app_container_cls = create_autospec(AppContainer)
        mock_lxc_service = Mock()
        mock_skeleton_assembler = Mock()
        mock_ancestor_info_cls = create_autospec(AncestorInfo)

        creator = AppContainerCreator(mock_settings,
                app_container_cls=mock_app_container_cls,
                lxc_service=mock_lxc_service,
                skeleton_assembler=mock_skeleton_assembler,
                ancestor_info_cls=mock_ancestor_info_cls)
        self.creator = creator

        self.mock_settings = mock_settings
        self.mock_app_container_cls = mock_app_container_cls
        self.mock_lxc_service = mock_lxc_service
        self.mock_skeleton_assembler = mock_skeleton_assembler
        self.mock_ancestor_info_cls = mock_ancestor_info_cls

    @patch('appcontainers.creator.Directory')
    def test_app_container_creator_provision_container(self, mock_dir_cls):
        fake_reservation = FakeResourceReservation.create('somename',
                '192.168.0.1', '00:16:3e:00:00:00')
        container = self.creator.provision_container('base', fake_reservation)

        # Mock Assertions
        mock_lxc = self.mock_lxc_service.create.return_value
        self.mock_skeleton_assembler.setup.assert_called_with(
                self.mock_settings,
                mock_lxc,
                fake_reservation)

        mock_dir_cls.make.assert_called_with(
                self.mock_settings.overlays_path.return_value)

        self.mock_ancestor_info_cls.create.assert_called_with('base')

        # Assert return value
        assert container == self.mock_app_container_cls.create.return_value

        self.mock_app_container_cls.create.assert_called_with(
                self.mock_ancestor_info_cls.create.return_value,
                mock_lxc, fake_reservation)
