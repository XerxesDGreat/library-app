from django.test import TestCase
from models import Patron

class ModelTest(TestCase):
    def test_student_full_name(self):
        a = Patron(first_name='asdf', last_name='qwer')
        self.assertEqual('asdf qwer', a.full_name())
    

class PatronTest(TestCase):
    def test_is_staff(self):
        for t, is_staff in [('S', False), ('P', False), ('A', True), ('T', True)]:
            a = Patron(type=t)
            self.assertEqual(is_staff, a.is_staff())