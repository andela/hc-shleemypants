from django.contrib.auth.models import User

from hc.api.models import Check
from hc.test import BaseTestCase
from datetime import timedelta as td
from django.utils import timezone
from hc.front.forms import PriorityForm


class MyChecksTestCase(BaseTestCase):

    def setUp(self):
        super(MyChecksTestCase, self).setUp()
        self.check = Check(user=self.alice, name="Alice Was Here")
        self.check.save()

    def test_it_works(self):
        for email in ("alice@example.org", "bob@example.org"):
            self.client.login(username=email, password="password")
            r = self.client.get("/checks/")
            self.assertContains(r, "Alice Was Here", status_code=200)

    def test_it_shows_green_check(self):
        self.check.last_ping = timezone.now()
        self.check.status = "up"
        self.check.save()

        self.client.login(username="alice@example.org", password="password")
        r = self.client.get("/checks/")

        # Desktop
        self.assertContains(r, "icon-up")
    #
        # Mobile
        self.assertContains(r, "label-success")

    def test_it_shows_red_check(self):
        self.check.last_ping = timezone.now() - (td(days=1) + td(hours=1))
        self.check.status = "up"
        self.check.save()

        self.client.login(username="alice@example.org", password="password")
        r = self.client.get("/checks/")

        # Desktop
        self.assertContains(r, "icon-down")

        # Mobile
        self.assertContains(r, "label-danger")

    def test_it_shows_amber_check(self):
        self.check.last_ping = timezone.now() - td(days=1, minutes=30)
        self.check.status = "up"
        self.check.save()

        self.client.login(username="alice@example.org", password="password")
        r = self.client.get("/checks/")

        # Desktop
        self.assertContains(r, "icon-grace")

        # Mobile
        self.assertContains(r, "label-warning")


    def test_it_counts_renders_unresolved_checks(self):
        self.check.last_ping = timezone.now() - (td(days=1) + td(hours=1))
        self.check.status = "up"
        self.check.save()

        self.client.login(username="alice@example.org", password="password")
        r = self.client.get("/checks/")

        self.assertEqual(len(r.context[0]["unresolved"]), 1)

    def test_it_counts_running_checks(self):
        self.check.last_ping = timezone.now()
        self.check.status = "up"
        self.check.save()

        check2 = Check(user=self.alice, name="Monitor my db update")
        check2.last_ping = timezone.now()
        check2.status = "up"
        check2.save()

        self.client.login(username="alice@example.org", password="password")
        r = self.client.get("/checks/")
        self.assertEqual(len(r.context[0]["up"]), 2)

    def test_it_shows_no_checks_when_empty(self):
        samjunior = User(username="samaki", email="samjunior@fishnet.com")
        samjunior.set_password("password")
        samjunior.save()

        self.client.login(username="samjunior@fishnet.com", password="password")
        r = self.client.get("/checks/")
        self.assertContains(r, 'You don\'t have any checks yet.')

    def test_it_shows_no_checks_running_when_empty(self):
        samjunior = User(username="samaki", email="samjunior@fishnet.com")
        samjunior.set_password("password")
        samjunior.save()

        self.check.last_ping = timezone.now() - (td(days=1) + td(hours=1))
        self.check.user = samjunior
        self.check.status = "up"
        self.check.save()

        self.client.login(username="samjunior@fishnet.com", password="password")
        r = self.client.get("/checks/")

        self.assertContains(r, 'You don\'t have any running checks.')

    def test_it_shows_no_checks_unresolved_when_empty(self):
        samjunior = User(username="samaki", email="samjunior@fishnet.com")
        samjunior.set_password("password")
        samjunior.save()

        self.check.last_ping = timezone.now()
        self.check.user = samjunior
        self.check.status = "up"
        self.check.save()

        self.client.login(username="samjunior@fishnet.com", password="password")
        r = self.client.get("/checks/")
        self.assertContains(r, 'You don\'t have any unresolved checks')

    def test_default_priority_is_normal(self):
        self.client.login(username="alice@example.org", password="password")
        self.assertEqual(self.check.priority, 0)
        self.assertEqual(self.check.priority_name, 'normal')

    def test_it_sets_priority(self):
        self.client.login(username="alice@example.org", password="password")
        self.check.priority  = 1
        self.check.save()
        self.client.post("/checks/{}/priority/".format(self.check.code),{'selected_priority':2})
        self.check.refresh_from_db()
        self.assertEqual(self.check.priority, 2)


