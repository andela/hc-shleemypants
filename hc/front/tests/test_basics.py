from django.test import TestCase

from hc.api.models import Check


class BasicsTestCase(TestCase):

    def test_it_shows_welcome(self):
        r = self.client.get("/")
        self.assertContains(r, "Get Notified", status_code=200)

    def test_welcome_code(self):
        r = self.client.get("/")
        code = self.client.session["welcome_code"]
        self.assertIsNotNone(Check.objects.filter(code=code))

        self.client.session["welcome_code"] = "x"
        r = self.client.get("/")
        code = self.client.session["welcome_code"]
        self.assertEqual(r.status_code, 200)
        self.assertNotEqual(code, "x")
        self.assertIsNotNone(Check.objects.filter(code=code))
