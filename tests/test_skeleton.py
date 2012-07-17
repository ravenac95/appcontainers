from mock import Mock, patch, call
from appcontainers.skeleton import *
from tests.fakes import *


def test_initialize_skeleton_assembler():
    SkeletonAssembler()


class TestSkeletonAssembler(object):
    def setup(self):
        self.assembler = SkeletonAssembler()

    @patch('appcontainers.skeleton.SkeletonWriter', autospec=True)
    @patch('os.walk')
    def test_setup(self, mock_walk, mock_writer_cls):
        # FIXME this is a c/mplicated test :-/
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
