from datetime import timedelta

from django.test import TestCase
from django.utils import timezone
from hc.api.models import Check


class CheckModelTestCase(TestCase):

    def test_it_strips_tags(self):
        check = Check()

        check.tags = " foo  bar "
        self.assertEquals(check.tags_list(), ["foo", "bar"])
    
    def test_it_strips_empty_tags(self):
        check = Check()

        check.tags = "     "
        self.assertEquals(check.tags_list(), [])
 
        check.name = "";
        self.assertFalse(check.name)

    def test_status_works_with_grace_period(self):
        check = Check()

        check.status = "up"

        check.timeout = timedelta(days=1)
        check.grace = timedelta(hours=1)
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)

        self.assertTrue(check.in_grace_period())
        self.assertEqual(check.get_status(), "late")

        ### The above 2 asserts fail. Make them pass

    def test_paused_check_is_not_in_grace_period(self):
        check = Check()

        check.status = "up"
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)
        self.assertTrue(check.in_grace_period())

        check.status = "paused"
        self.assertFalse(check.in_grace_period())

    def test_new_check_is_not_in_grace_period(self):
        check = Check()
        check.status = "new"
        
        check.timeout = timedelta(days=1)
        check.grace = timedelta(hours=1)
        check.last_ping = timezone.now() - timedelta(days=1, minutes=30)

        self.assertFalse(check.in_grace_period())

    def test_send_alert(self):
        check = Check()

        if check.status not in ("up", "down", "often"):
            self.assertRaises(NotImplementedError, msg="Unexpected status")       
            
