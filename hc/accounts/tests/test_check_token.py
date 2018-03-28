from django.contrib.auth.hashers import make_password
from hc.test import BaseTestCase


class CheckTokenTestCase(BaseTestCase):

    def setUp(self):
        super(CheckTokenTestCase, self).setUp()
        self.profile.token = make_password("secret-token")
        self.profile.save()

    def test_it_shows_form(self):
        r = self.client.get("/accounts/check_token/alice/secret-token/")
        self.assertContains(r, "You are about to log in")

    def test_it_redirects(self):
        r = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(r, "/checks/")

        # After login, token should be blank
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.token, "")

    ### Login and test it redirects already logged in
    def test_it_redirects_already_logged_in(self):
        # send request to login
        self.client.login(username="alice@example.org", password="password")

        res = self.client.post("/accounts/check_token/alice/secret-token/")
        self.assertRedirects(res, "/checks/")


    ### Login with a bad token and check that it redirects
    def test_it_redirects_bad_login(self):
        #set follow to true in order to follow redirects
        res = self.client.post("/accounts/check_token/alice/invalid-token/", follow=True)
        self.assertRedirects(res, "/accounts/login/")
        self.assertContains(res, "incorrect or expired")

    ### Any other tests?
