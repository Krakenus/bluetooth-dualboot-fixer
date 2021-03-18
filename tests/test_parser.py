from unittest import TestCase
from unittest.mock import patch

from btfix.parser import _rename_dir


def mocked_rename(*args, **kwargs):
    pass


class ParserTestCase(TestCase):

    @patch('os.rename', mocked_rename)
    def test_rename_dir(self):
        mac = 'AA:BB:CC:DD:EE:FF'
        path = '/some/path/to/file'
        expected = f'/some/path/{mac}/file'

        self.assertEqual(_rename_dir(path, mac), expected)
