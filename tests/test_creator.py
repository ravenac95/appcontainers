from mock import Mock, patch, create_autospec
from appcontainers.creator import *
from tests.fakes import *


class TestAppContainerCreator(object):
    def setup(self):
        from appcontainers.models import AppContainer
        mock_settings = Mock()
        mock_app_container_cls = create_autospec(AppContainer)
        mock_lxc_service = Mock()
        mock_skeleton_assembler = Mock()

        creator = AppContainerCreator(mock_settings,
                lxc_service=mock_lxc_service,
                skeleton_assembler=mock_skeleton_assembler,
                app_container_cls=mock_app_container_cls)
        self.creator = creator

        self.mock_settings = mock_settings
        self.mock_app_container_cls = mock_app_container_cls
        self.mock_lxc_service = mock_lxc_service
        self.mock_skeleton_assembler = mock_skeleton_assembler

    @patch('appcontainers.creator.Directory')
    def test_app_container_creator_provision_container(self, mock_dir_cls):
        fake_metadata = FakeAppContainerMetadata.create('somename',
                '192.168.0.1', '00:16:3e:00:00:00', 'base')
        container = self.creator.provision_container(fake_metadata)

        # Mock Assertions
        mock_lxc = self.mock_lxc_service.create.return_value
        self.mock_skeleton_assembler.setup.assert_called_with(
                self.mock_settings,
                mock_lxc,
                fake_metadata)

        mock_dir_cls.make.assert_called_with(
                self.mock_settings.overlays_path.return_value)

        # Assert return value
        assert container == self.mock_app_container_cls.create.return_value

        self.mock_app_container_cls.create.assert_called_with(
                mock_lxc, fake_metadata)
