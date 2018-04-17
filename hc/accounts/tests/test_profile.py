from django.core import mail

from hc.test import BaseTestCase
from hc.accounts.models import Member
from hc.api.models import Check


class ProfileTestCase(BaseTestCase):

    def test_it_sends_set_password_link(self):
        self.client.login(username="alice@example.org", password="password")

        form = {"set_password": "1"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 302

        # profile.token should be set now
        self.alice.profile.refresh_from_db()
        token = self.alice.profile.token
        self.assertFalse(token is None)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Set password on healthchecks.io')
        self.assertIn( 'Here\'s a link to set a password', mail.outbox[0].body)
        self.assertRedirects(r, "/accounts/set_password_link_sent/")

    def test_it_sends_report(self):
        #login user
        self.client.login(username="alice@example.org", password="password")

        check = Check(name="Test Check", user=self.alice)
        check.save()

        form = {"update_reports_allowed":"1" ,"report_freqs": "immediately"}
        r = self.client.post("/accounts/profile/", form)
        self.assertEquals(200,  r.status_code)

        self.alice.profile.send_report(7)

        self.assertGreater(len(mail.outbox), 0)
        self.assertIn(mail.outbox[0].subject, "Recent Reports")

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn( 'This is a monthly report sent by healthchecks.io.',mail.outbox[0].body)
        self.assertIn( 'Test Check',mail.outbox[0].body)

    def test_it_adds_team_member(self):
        self.client.login(username="alice@example.org", password="password")

        form = {"invite_team_member": "1", "email": "frank@example.org"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 200

        member_emails = set()
        for member in self.alice.profile.member_set.all():
            member_emails.add(member.user.email)

        self.assertTrue("frank@example.org" in member_emails)

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn( 'alice@example.org invites you to',mail.outbox[0].body)


    def test_add_team_member_checks_team_access_allowed_flag(self):
        self.client.login(username="charlie@example.org", password="password")

        form = {"invite_team_member": "1", "email": "frank@example.org"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 403

    def test_it_removes_team_member(self):
        self.client.login(username="alice@example.org", password="password")

        form = {"remove_team_member": "1", "email": "bob@example.org"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 200

        self.assertEqual(Member.objects.count(), 0)

        self.bobs_profile.refresh_from_db()
        self.assertEqual(self.bobs_profile.current_team, None)

    def test_it_sets_team_name(self):
        self.client.login(username="alice@example.org", password="password")

        form = {"set_team_name": "1", "team_name": "Alpha Team"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 200

        self.alice.profile.refresh_from_db()
        self.assertEqual(self.alice.profile.team_name, "Alpha Team")

    def test_set_team_name_checks_team_access_allowed_flag(self):
        self.client.login(username="charlie@example.org", password="password")

        form = {"set_team_name": "1", "team_name": "Charlies Team"}
        r = self.client.post("/accounts/profile/", form)
        assert r.status_code == 403

    def test_it_switches_to_own_team(self):
        self.client.login(username="bob@example.org", password="password")

        self.client.get("/accounts/profile/")

        # After visiting the profile page, team should be switched back
        # to user's default team.
        self.bobs_profile.refresh_from_db()
        self.assertEqual(self.bobs_profile.current_team, self.bobs_profile)

    def test_it_shows_badges(self):
        self.client.login(username="alice@example.org", password="password")
        Check.objects.create(user=self.alice, tags="foo a-B_1  baz@")
        Check.objects.create(user=self.bob, tags="bobs-tag")

        r = self.client.get("/accounts/profile/")
        self.assertContains(r, "foo.svg")
        self.assertContains(r, "a-B_1.svg")

        # Expect badge URLs only for tags that match \w+
        self.assertNotContains(r, "baz@.svg")

        # Expect only Alice's tags
        self.assertNotContains(r, "bobs-tag.svg")

    def test_it_creates_api_key(self):
        self.client.login(username="alice@example.org", password="password")
        #include create_api_key in request
        form = {"create_api_key": "1"}
        r = self.client.post("/accounts/profile/", form)
        self.assertEqual(r.status_code, 200)
        self.profile.refresh_from_db()
        api_key = self.profile.api_key
        self.assertFalse(api_key is None)
