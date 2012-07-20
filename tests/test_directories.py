from mock import Mock, patch
from appcontainers.directories import *


def test_directory_list_destroy():
    mock_dir1 = Mock()
    mock_dir2 = Mock()

    directory_list = DirectoryList([mock_dir1, mock_dir2])
    directory_list.destroy()

    mock_dir1.destroy.assert_called_with()
    mock_dir2.destroy.assert_called_with()


@patch('os.mkdir')
@patch('os.path')
def test_directory_make(mock_path, mock_mkdir):
    directory = Directory.make('/hello')

    fake_abspath_return = mock_path.abspath.return_value

    mock_path.abspath.assert_called_with('/hello')
    mock_mkdir.assert_called_with(fake_abspath_return)

    assert directory.path == fake_abspath_return
