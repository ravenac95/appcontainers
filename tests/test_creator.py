from mock import Mock, patch, call
from appcontainers.creator import *
from tests.fakes import *


class TestAppContainerCreator(object):
    def setup(self):
        mock_settings = Mock()
        mock_app_container_cls = Mock()
        mock_lxc_service = Mock()
        mock_file_assembler = Mock()

        creator = AppContainerCreator(mock_settings,
                app_container_cls=mock_app_container_cls,
                lxc_service=mock_lxc_service,
                file_assembler=mock_file_assembler)
        self.creator = creator

        self.mock_settings = mock_settings
        self.mock_app_container_cls = mock_app_container_cls
        self.mock_lxc_service = mock_lxc_service
        self.mock_file_assembler = mock_file_assembler

    def test_app_container_creator_provision_container(self):
        fake_reservation = FakeResourceReservation.create('somename',
                '192.168.0.1', '00:16:3e:00:00:00')
        container = self.creator.provision_container('base', fake_reservation)
        # Mock Assertions
        self.mock_file_assembler.setup.assert_called_with(
                self.mock_settings,
                self.mock_lxc_service.create.return_value,
                fake_reservation)

        # Assert return value
        assert container == self.mock_app_container_cls.create.return_value


def test_initialize_file_assembler():
    FileAssembler()


class TestFileAssembler(object):
    def setup(self):
        self.assembler = FileAssembler()

    @patch('appcontainers.creator.LXCSkeletonWriter', autospec=True)
    @patch('os.walk')
    def test_setup(self, mock_walk, mock_writer_cls):
        # FIXME this is a complicated test :-/
        mock_settings = Mock()
        mock_lxc = Mock()
        mock_reservation = Mock()

        # Setup Writer
        mock_writer = mock_writer_cls.return_value

        # Setup settings
        mock_settings.skeletons_path.return_value = '/base'

        # Fake walk return values
        mock_walk.return_value = [
            ('/base/somedir', ['hello'], ['one.sh.tmpl']),
            ('/base/somedir/hello', [], ['hello.tmpl', 'world']),
        ]

        self.assembler.setup(mock_settings, mock_lxc, mock_reservation)

        #### LXCSkeletonWriter.render assertions

        # Expected render calls
        common_kwargs = dict(lxc=mock_lxc, settings=mock_settings,
                reservation=mock_reservation)
        expected_render_calls = [
            call('somedir/one.sh.tmpl', **common_kwargs),
            call('somedir/hello/hello.tmpl', **common_kwargs),
        ]
        # Order shouldn't matter as long as all the files are made correctly
        mock_writer.render.assert_has_calls(expected_render_calls, any_order=True)

        #### LXCSkeletonWriter.copy assertions
        expected_copy_calls = [
            call('somedir/hello/world'),
        ]
        mock_writer.copy.assert_has_calls(expected_copy_calls, any_order=True)

        #### LXCSkeletonWriter.make_dir assertions
        expected_ensure_dir_calls = [
            call('somedir/hello'),
        ]
        mock_writer.ensure_dir.assert_has_calls(expected_ensure_dir_calls)
