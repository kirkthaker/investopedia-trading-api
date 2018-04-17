from unittest import TestCase, main
from InvestopediaApi import ita
from test.config import test_username, test_password


class LoginTestCase(TestCase):
    def test_notify_invalid_login(self):
        with self.assertRaises(ita.LoginError) as context:
            ita.Account(test_username, 'invalidpassword')

        self.assertTrue("Login Error: Invalid Username or Password" in str(context.exception))

    def test_valid_login(self):
        client = ita.Account(test_username, test_password)

        self.assertTrue(client.logged_in)


if __name__ == '__main__':
    main()
