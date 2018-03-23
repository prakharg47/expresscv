from django.test import TestCase
import unittest
import publish.utils as utils
# Create your tests here.

class UtilsTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_email_unescape(self):
        self.assertEqual(utils.unescape_email("prakhar_11509@gmail.com"), "prakhar\\_11509@gmail.com" )
