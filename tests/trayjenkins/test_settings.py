import mox
from unittest import TestCase

from trayjenkins.settings import Settings, CommandLineSettingsParser


class SettingsTests(TestCase):

    def test_Equality_operator___Two_identical_objects___Return_true(self):

        one = Settings('host', username='username', password='password')
        two = Settings('host', username='username', password='password')

        self.assertTrue(one == two)

    def test_Equality_operator___Host_differs___Return_false(self):

        one = Settings('host', username='username', password='password')
        two = Settings('other host', username='username', password='password')

        self.assertFalse(one == two)

    def test_Equality_operator___Username_differs___Return_false(self):

        one = Settings('host', username='username', password='password')
        two = Settings('host', username='arthur', password='password')

        self.assertFalse(one == two)

    def test_Equality_operator___Password_differs___Return_false(self):

        one = Settings('host', username='username', password='password')
        two = Settings('host', username='username', password='camelot')

        self.assertFalse(one == two)

    def test_Equality_operator___Compare_with_None___Return_false(self):

        settings = Settings('host', username='username', password='password')

        self.assertFalse(settings == None)

    def test_repr_ReturnsSensibleResult(self):

        settings = Settings('camelot', username='arthur', password='silly place')
        expected = "Settings(host='camelot',username='arthur',password='silly place')"
        self.assertEquals(expected, settings.__repr__())


class CommandLineSettingsParserTests(TestCase):

    def test_parse___Empty_list___Return_None(self):

        expected = None
        parser = CommandLineSettingsParser()
        result = parser.parse([])

        self.assertEquals(expected, result)

    def test_parse___Just_host___Return_appropriate_settings(self):

        expected = Settings('hostname')
        parser = CommandLineSettingsParser()
        result = parser.parse(['hostname'])

        self.assertEquals(expected, result)

    def test_parse___Just_username_with_minus_u_and_host___Return_appropriate_settings(self):

        expected = Settings('hostname', username='sir robin')
        parser = CommandLineSettingsParser()
        result = parser.parse(['-u', 'sir robin', 'hostname'])

        self.assertEquals(expected, result)

    def test_parse___Just_username_with_minus_minus_username_and_host___Return_appropriate_settings(self):

        expected = Settings('hostname', username='sir robin')
        parser = CommandLineSettingsParser()
        result = parser.parse(['--username', 'sir robin', 'hostname'])

        self.assertEquals(expected, result)

    def test_parse___Just_password_with_minus_p_and_host___Return_appropriate_settings(self):

        expected = Settings('hostname', password='aramathea')
        parser = CommandLineSettingsParser()
        result = parser.parse(['-p', 'aramathea', 'hostname'])

        self.assertEquals(expected, result)

    def test_parse___Just_username_with_minus_minus_password_and_host___Return_appropriate_settings(self):

        expected = Settings('hostname', password='aramathea')
        parser = CommandLineSettingsParser()
        result = parser.parse(['--password', 'aramathea', 'hostname'])

        self.assertEquals(expected, result)
