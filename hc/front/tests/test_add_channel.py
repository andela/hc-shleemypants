from django.contrib.auth.models import User
from django.test.utils import override_settings

from hc.accounts.models import Profile
from hc.api.models import Channel
from hc.test import BaseTestCase


@override_settings(PUSHOVER_API_TOKEN="token", PUSHOVER_SUBSCRIPTION_URL="url")
class AddChannelTestCase(BaseTestCase):

    def test_it_adds_email(self):
        url = "/integrations/add/"
        form = {"kind": "email", "value": "alice@example.org"}

        self.client.login(username="alice@example.org", password="password")
        r = self.client.post(url, form)
        user = User.objects.get(email='alice@example.org')

        self.assertRedirects(r, "/integrations/")
        self.assertEqual(Channel.objects.count(), 1)
        self.assertEqual('alice@example.org', user.email)

    def test_it_trims_whitespace(self):
        """ Leading and trailing whitespace should get trimmed. """
        url = "/integrations/add/"
        form = {"kind": "email", "value": "   alice@example.org   "}

        self.client.login(username="alice@example.org", password="password")
        self.client.post(url, form)

        q = Channel.objects.filter(value="alice@example.org")
        self.assertEqual(q.count(), 1)

    def test_instructions_work(self):
        self.client.login(username="alice@example.org", password="password")
        kinds = ("email", "webhook", "pd", "pushover", "hipchat", "victorops")
        for frag in kinds:
            url = "/integrations/add_%s/" % frag
            r = self.client.get(url)
            self.assertContains(r, "Integration Settings", status_code=200)

    def test_bad_kinds_dont_work(self):
        """Should not work since , the kinds are invalid"""
        self.client.login(username="alice@example.org", password="password")
        kinds = ("fish", "new", "mpesa")
        for frag in kinds:
            url = "/integrations/add_{}/".format(frag)
            r = self.client.get(url)
            self.assertContains(r, frag, status_code=404)

    def test_team_access_works(self):
        # creating Junior as new user and adding him to team
        self.junior = User(username="junior", email="junor@younggeeks.com")
        self.junior.set_password("secret")
        self.junior.save()

        # allow team access
        self.profile = Profile(user=self.junior, api_key="thisisawesomesecretkey")
        self.profile.team_access_allowed = True
        self.profile.team_name = "GEEKS"
        self.profile.save()

        self.zachary = User(username="zachary", email="zachary@younggeeks.com")
        self.zachary.set_password("password")
        self.zachary.save()

        # Adding zachary to the same team as junior(TEAM GEEKS)
        self.zachary_profile = Profile(user=self.zachary, api_key="newawesomesupersecurekey")
        self.zachary_profile.current_team = self.profile
        self.zachary_profile.save()

        self.assertEqual(True, self.profile.team_access_allowed)
        self.assertEqual("thisisawesomesecretkey", self.zachary_profile.current_team.api_key)
