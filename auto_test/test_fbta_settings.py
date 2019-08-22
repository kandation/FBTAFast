import unittest

from fbta_settings import FBTASettings


class TestFBTASettingsBasic(unittest.TestCase):

    def test_empty_username(self):
        with self.assertRaises(ValueError) as e:
            assert FBTASettings('','.')
        assert str(e.exception) == 'Username MUST not empty'

    def test_static_variable(self):
        s = FBTASettings('testusername','.')

        with self.assertRaises(Exception) as e:
            s.DIR_DETAIL_NEW_ALL_RUN = 'dir_detail_new_all_run_2'
            s.DIR_DETAIL_NEW_ON_DAY = 'dir_detail_new_all_run_2'
        self.assertTrue(str(e.exception),'can\'t set attribute')
        self.assertTrue(s.DIR_DETAIL_NEW_ALL_RUN,'dir_detail_new_all_run')

    def test_generate_db(self):
        s = FBTASettings('testusername', '.')
        assert s.db_name[0:5] == 'fbta_'


