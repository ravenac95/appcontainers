import filecmp
from mock import Mock, patch, call, ANY
from nose.plugins.attrib import attr
from testkit import temp_directory
from appcontainers.skeleton import *
from tests import fixtures_path
from tests.fakes import *


def test_initialize_skeleton_assembler():
    SkeletonAssembler()


class TestSkeletonAssembler(object):
    def setup(self):
        self.assembler = SkeletonAssembler()

    @patch('appcontainers.skeleton.SkeletonWriter', autospec=True)
    @patch('os.walk')
    def test_setup(self, mock_walk, mock_writer_cls):
        # FIXME this is a complicated test :-/
        mock_settings = Mock()
        mock_lxc = Mock()
        mock_metadata = Mock()

        # Setup Writer
        mock_writer = mock_writer_cls.return_value

        # Setup settings
        mock_settings.skeletons_path.return_value = '/base'

        # Fake walk return values
        mock_walk.return_value = [
            ('/base/somedir', ['hello'], ['one.sh.tmpl']),
            ('/base/somedir/hello', [], ['hello.tmpl', 'world']),
        ]

        self.assembler.setup(mock_settings, mock_lxc, mock_metadata)

        #### SkeletonWriter.render assertions

        # Expected render calls
        common_kwargs = dict(ext_length=ANY, metadata=mock_metadata)
        expected_render_calls = [
            call('somedir/one.sh.tmpl', **common_kwargs),
            call('somedir/hello/hello.tmpl', **common_kwargs),
        ]
        # Order shouldn't matter as long as all the files are made correctly
        mock_writer.render.assert_has_calls(expected_render_calls,
                any_order=True)

        #### SkeletonWriter.copy assertions
        expected_copy_calls = [
            call('somedir/hello/world'),
        ]
        mock_writer.copy.assert_has_calls(expected_copy_calls, any_order=True)

        #### SkeletonWriter.make_dir assertions
        expected_ensure_dir_calls = [
            call('somedir/hello'),
        ]
        mock_writer.ensure_dir.assert_has_calls(expected_ensure_dir_calls)


class TestSkeletonWriter(object):
    def setup(self):
        self.writer = SkeletonWriter('/base', '/lxc')

    def test_generate_path_pair(self):
        tests = [
            (('hello', 0), ('/base/hello', '/lxc/hello')),
            (('hello/there.tmpl', 5), ('/base/hello/there.tmpl',
                '/lxc/hello/there')),
        ]
        for test_args, expected in tests:
            yield self.do_generate_path_pair, test_args, expected

    def do_generate_path_pair(self, test_args, expected):
        path_pair = self.writer.generate_path_pair(*test_args)
        assert path_pair == expected

    @patch('__builtin__.open')
    @patch('tempita.Template')
    def test_render(self, mock_template_cls, mock_file_open):
        test_context = dict(a=1, b=2, c='c')
        self.writer.render('hello.tmpl', ext_length=5, **test_context)

        mock_template_cls.from_filename.assert_called_with('/base/hello.tmpl')
        (mock_template_cls.from_filename.return_value
                .substitute.assert_called_with(**test_context))
        mock_file_open.assert_called_with('/lxc/hello', 'w')

    @patch('shutil.copy')
    def test_copy(self, mock_copy):
        self.writer.copy('hello.there')
        mock_copy.assert_called_with('/base/hello.there', '/lxc/hello.there')

    @patch('os.mkdir')
    def test_ensure_dir_new(self, mock_mkdir):
        self.writer.ensure_dir('hellodir')
        mock_mkdir.assert_called_with('/lxc/hellodir')

    @patch('os.mkdir')
    def test_ensure_dir_with_os_error(self, mock_mkdir):
        mock_mkdir.side_effect = OSError()
        self.writer.ensure_dir('hellodir')


@attr('medium')
class TestSkeletonAssemblerWithFixtures(object):
    """Test the SkeletonWriter with Fixture data"""
    def setup_skeleton1(self, temp_dir, skeleton1_input):
        # Setup fake settings
        mock_settings = Mock()
        mock_settings.skeletons_path.return_value = skeleton1_input

        # Setup fake LXC
        mock_lxc = Mock()
        mock_lxc.path.return_value = temp_dir

        # Fake Reservation
        fake_metadata = FakeAppContainerMetadata('SOMENAME',
                '192.168.0.1', '00:16:3e:00:00:01', 'base')

        return (mock_settings, mock_lxc, fake_metadata)

    def assert_identical_dirs(self, test_dir, expected_dir, message=None):
        comparison = filecmp.dircmp(test_dir, expected_dir)

        if (comparison.diff_files or comparison.right_only
                or comparison.left_only):
            raise AssertionError('Directories do not match')

    def test_with_skeleton1_fixture(self):
        skeleton1_input = fixtures_path('skeleton1/input')
        skeleton1_expected = fixtures_path('skeleton1/expected')
        with temp_directory() as temp_dir:
            setup_args = self.setup_skeleton1(temp_dir, skeleton1_input)

            assembler = SkeletonAssembler()
            assembler.setup(*setup_args)

            self.assert_identical_dirs(temp_dir, skeleton1_expected)

    def test_with_skeleton1_fixture_write_multiple_times(self):
        """Test that the assembler can be run multiple times and produce the
        same result
        """
        skeleton1_input = fixtures_path('skeleton1/input')
        skeleton1_expected = fixtures_path('skeleton1/expected')
        with temp_directory() as temp_dir:
            setup_args = self.setup_skeleton1(temp_dir, skeleton1_input)

            assembler = SkeletonAssembler()

            # Run multiple times
            assembler.setup(*setup_args)
            assembler.setup(*setup_args)
            assembler.setup(*setup_args)

            self.assert_identical_dirs(temp_dir, skeleton1_expected)
