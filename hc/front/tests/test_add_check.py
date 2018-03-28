from hc.api.models import Check
from hc.test import BaseTestCase


class AddCheckTestCase(BaseTestCase):

    def test_it_works(self):
        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url)
        self.assertRedirects(r, "/checks/")
        assert Check.objects.count() == 1

    ## Test that team access works
    def test_team_access_works(self):
        url = "/checks/add/"
        self.client.login(username="alice@example.org", password="password")
        res = self.client.post(url)
        self.client.logout()

        self.client.login(username="bob@example.org", password="password")
        self.client.post(url)
        assert Check.objects.count() == 2

    def test_unauthorized_access_doesnt_work(self):
        """
            Test if unauthorized user can add check
        """
        url = "/checks/add/"
        res = self.client.post(url)
        assert res.status_code == 302
        